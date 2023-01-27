import os 

from pytorch_lightning import LightningDataModule
from torch_geometric.loader import DataLoader
import torch_geometric.transforms as T

from components.datasets import MolDataset
from components.transformQM import GNNTransformQM

class QMDataModule(LightningDataModule):
    """A DataModule implements 4 key methods:

        def setup(self, stage):
            # things to do on every process
            # load data, set variables, etc...
        def train_dataloader(self):
            # return train dataloader
        def val_dataloader(self):
            # return validation dataloader
        def test_dataloader(self):
            # return test dataloader
    """

    def __init__(
        self,
        files_root: str,
        fold: int,
        batch_size = 128,
        num_workers = 48,
        transform = T.RandomTranslate(0.05)
    ):
        super().__init__()

        # this line allows to access init params with 'self.hparams' attribute
        # also ensures init params will be stored in ckpt
        self.save_hyperparameters(logger=False)

        self.files_root = files_root

        self.fold = fold

        self.batch_size = batch_size
        self.num_workers = num_workers

        self.transform = transform 

    def setup(self):
        """Load data. Set variables: `self.data_train`, `self.data_val`, `self.data_test`.

        """

        self.data_train = MolDataset(os.path.join(self.files_root, "h5_files/qm.hdf5"), os.path.join(self.files_root, "splits/train_norm_fold{}.txt".format(self.fold)), target_norm_file=os.path.join(self.files_root, "h5_files/qm_norm_fold{}.hdf5".format(self.fold)), transform=GNNTransformQM(), post_transform=self.transform)
        self.data_val = MolDataset(os.path.join(self.files_root, "h5_files/qm.hdf5"), os.path.join(self.files_root, "splits/val_norm_fold{}.txt".format(self.fold)), target_norm_file=os.path.join(self.files_root, "h5_files/qm_norm_fold{}.hdf5".format(self.fold)), transform=GNNTransformQM())
        self.data_test = MolDataset(os.path.join(self.files_root, "h5_files/qm.hdf5"), os.path.join(self.files_root, "splits/test_norm_fold{}.txt".format(self.fold)), target_norm_file=os.path.join(self.files_root, "h5_files/qm_norm_fold{}.hdf5".format(self.fold)), transform=GNNTransformQM())

    def train_dataloader(self):
        return DataLoader(
            dataset=self.data_train, 
            batch_size=self.batch_size, 
            shuffle=True, 
            num_workers=self.num_workers
        )

    def val_dataloader(self):
        return DataLoader(
            dataset=self.data_val, 
            batch_size=self.batch_size, 
            shuffle=False, 
            num_workers=self.num_workers
        )

    def test_dataloader(self):
        return DataLoader(
            dataset=self.data_test, 
            batch_size=self.batch_size, 
            shuffle=False, 
            num_workers=self.num_workers
        )

if __name__ == "__main__":
    _ = QMDataModule()
