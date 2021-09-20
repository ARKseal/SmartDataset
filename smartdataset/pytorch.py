try:
    from torch.utils.data import DataLoader, IterableDataset
except ModuleNotFoundError:
    class IterableDataset:
        pass

    class DataLoader:
        pass
