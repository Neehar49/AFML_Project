import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader
import numpy as np

from meta_model import FullModel, YieldDataset

def main():

    df = pd.read_csv("../data/meta_learning_dataset.csv")
    crops = sorted(df["crop"].unique())
    crop_to_idx = {c: i for i, c in enumerate(crops)}

    # Held-out region for Few-Shot Meta test
    held_out = "Thanjavur_TN"  # Change to test other regions

    support_years = [2015, 2016, 2017]  # few-shot training
    test_years = sorted(list(
        set(df[df["region"] == held_out]["year"]) - set(support_years)
    ))

    df_support = df[(df["region"] == held_out) & (df["year"].isin(support_years))]
    df_test    = df[(df["region"] == held_out) & (df["year"].isin(test_years))]

    # Load model
    ckpt = torch.load("../data/shared_encoder.pt", map_location="cpu")
    input_dim = 6 + len(crops)
    model = FullModel(input_dim)
    model.load_state_dict(ckpt["state_dict"])

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Freeze encoder → ANIL 
    for p in model.encoder.parameters():
        p.requires_grad = False

    support_ds = YieldDataset(df_support, crop_to_idx)
    test_ds    = YieldDataset(df_test, crop_to_idx)

    support_loader = DataLoader(support_ds, batch_size=len(support_ds), shuffle=True)
    test_loader    = DataLoader(test_ds, batch_size=len(test_ds), shuffle=False)

    loss_fn = nn.MSELoss()
    opt = optim.Adam(model.head.parameters(), lr=1e-2)

    # Adapt head on support set
    model.train()
    for ep in range(1, 101):
        for x, y, r in support_loader:
            x = x.to(device)
            y = y.to(device)

            opt.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            opt.step()

    # Evaluate on test years
    model.eval()
    preds, trues = [], []

    with torch.no_grad():
        for x, y, r in test_loader:
            x = x.to(device)
            y = y.to(device)
            pred = model(x)
            preds.extend(pred.cpu().numpy())
            trues.extend(y.cpu().numpy())

    preds = np.array(preds)
    trues = np.array(trues)

    mse = ((preds - trues) ** 2).mean()

    print("\n=== META-LEARNING EVALUATION ===")
    print("Held-out region:", held_out)
    print("Support years:", support_years)
    print("Test years:", test_years)
    print("Test MSE after fast adaptation:", mse)

if __name__ == "__main__":
    main()
