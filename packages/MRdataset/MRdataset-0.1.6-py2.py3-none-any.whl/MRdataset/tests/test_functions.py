from MRdataset.bids_utils import combine_entity_labels
import pytest

def test_combine_entity_labels():
    # Test case 1
    assert combine_entity_labels("sub-9001_ses-2_task-faces_bold.json",
                                 "anat") == "anat_task-faces_bold"

    # Test case 2
    assert combine_entity_labels("sub-9001_ses-2_T1w.nii.gz",
                                 "anat") == "anat_T1w"

    # Test case 3
    # with pytest.raises(AttributeError):
    #     combine_entity_labels("sub-9001_T1w.nii.gz", "labels")