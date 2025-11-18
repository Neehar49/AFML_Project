import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from torch.utils.data import DataLoader

from meta_model import YieldDataset, FullModel

def main():

    df = pd.read_csv("../data/meta_learning_dataset.csv")

    crops = sorted(df["crop"].unique())
    crop_to_idx = {c: i for i, c in enumerate(crops)}

    dataset = YieldDataset(df, crop_to_idx)
    loader  = DataLoader(dataset, batch_size=32, shuffle=True)

    input_dim = 6 + len(crops)     # 6 features + crop one-hot
    model = FullModel(input_dim)

    loss_fn = nn.MSELoss()
    opt = optim.Adam(model.parameters(), lr=1e-3)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    epochs = 50
    for ep in range(1, epochs+1):
        model.train()
        total = 0.0

        for x, y, r in loader:
            x = x.to(device)
            y = y.to(device)

            opt.zero_grad()
            pred = model(x)
            loss = loss_fn(pred, y)
            loss.backward()
            opt.step()

            total += loss.item() * x.size(0)

        print(f"Epoch {ep}: Loss = {total / len(dataset):.4f}")

    torch.save({
        "state_dict": model.state_dict(),
        "crop_to_idx": crop_to_idx
    }, "../data/shared_encoder.pt")

    print("Saved shared_encoder.pt")


if __name__ == "__main__":
    main()
