import numpy as np

from stytra import Stytra
from stytra.stimulation import Protocol
from stytra.stimulation.stimuli import Pause, CircleStimulus
from stytra.tracking.pipelines import Pipeline, ImageToDataNode, NodeOutput
from stytra.gui.camera_display import CameraViewWidget
from stytra.stimulation.estimators import Estimator

from deeplabcut.pose_estimation_tensorflow.config import load_config
from deeplabcut.pose_estimation_tensorflow.nnet.predict import getposeNP, setup_pose_prediction

from collections import namedtuple
from itertools import chain

import pyqtgraph as pg

video_file = r"C:\Users\vilim\programs\DeepLabCut\examples\openfield-Pranav-2018-10-30\videos\m3v1mp4.mp4"
dlc_cfg_file = r"C:\Users\vilim\programs\DeepLabCut\examples\openfield-Pranav-2018-10-30\dlc-models\iteration-0\openfieldOct30-trainset95shuffle1\test\pose_cfg.yaml"
model_snapshot_file = 'C:\\Users\\vilim\\programs\\DeepLabCut\\examples\\openfield-Pranav-2018-10-30\\dlc-models\\iteration-0\\openfieldOct30-trainset95shuffle1\\train\\snapshot-850000'


# We make a separate class to initialise and store the model." \
# It should be instantiated only on the tracking process"
class DLCmodel:
    def __init__(self, dlc_cfg_path, model_snapshot):
        self.dlc_cfg = load_config(dlc_cfg_path)
        self.dlc_cfg["init_weights"] = model_snapshot
        self.dlc_cfg['batch_size'] = 1
        self.sess, self.inputs, self.outputs = setup_pose_prediction(self.dlc_cfg)
        self.tracked_parts = self.dlc_cfg['all_joints_names']

    def predict_im(self, im):
        imfull = np.tile(im[:, :, None], (1, 1, 3))
        pose = getposeNP(imfull[None, :, :, :], self.dlc_cfg,
                  self.sess, self.inputs, self.outputs, outall=False)
        return pose.reshape(-1, 3)


# The tracking (image to data) node is subclassed to use the above defined model
class DLCNode(ImageToDataNode):
    def __init__(self, *args, dlc_cfg_path, model_path, **kwargs):
        super().__init__(*args, name="DLC_tracker",  **kwargs)
        self.dlc_cfg_path = dlc_cfg_path
        self.model_path = model_path
        self.model = None
        self._output_type = None

    def _process(self, image):
        # We put model instantiation here so it happens only on one process,
        # otherwise if it is in __init__, two tensorflow sessions would be
        # instantiated causing no end of problems
        if self.model is None:
            self.model = DLCmodel(self.dlc_cfg_path, self.model_path)
            self._output_type = namedtuple("o", chain.from_iterable(
                ([(p+"_x", p+"_y") for p in self.model.tracked_parts])))

        pose = self.model.predict_im(image)
        return NodeOutput([], self._output_type(*(pose[:, :2].flatten())))


# simple camera overlay which shows the positions of the tracked points
class DLCDisplay(CameraViewWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points_tracked = pg.ScatterPlotItem(
            size=10, pxMode=True, brush=(255, 0, 0), pen=None
        )
        self.display_area.addItem(self.points_tracked)

    def retrieve_image(self):
        super().retrieve_image()

        if len(self.experiment.acc_tracking.stored_data) == 0 or \
                self.current_image is None:
            return

        current_data = self.experiment.acc_tracking.values_at_abs_time(
            self.current_frame_time)

        points_plot = np.array(current_data).reshape(-1, 2)

        self.points_tracked.setData(x=points_plot[:, 0], y=points_plot[:, 1])


# the pipeline has only one tracking node
class MouseTrackPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self.display_overlay = DLCDisplay
        self.tracker = DLCNode(parent=self.root,
                               dlc_cfg_path=dlc_cfg_file,
                               model_path=model_snapshot_file)


# a simple estimator that just takes the snout position from the tracking data
class SnoutPositionEstimator(Estimator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data_type = namedtuple("o", "x y")

    def get_position(self):
        if len(self.acc_tracking.stored_data) > 0:
            last_pos = self.acc_tracking.stored_data[-1]
            return self._data_type(last_pos.snout_x, last_pos.snout_y)
        else:
            return self._data_type(-1, -1)


# a stimulus which draws a circle at the position of the snout
# there is no transform, since this is a virtual experiment, in reality
# one would also use a calibration matrix after obtaining the coordinates
class PosTrackingStimulus(CircleStimulus):
    def update(self):
        self.x, self.y = self._experiment.estimator.get_position()
        super().update()


class RatProtocol(Protocol):
    name = "follow the rat"
    stytra_config = dict(camera=dict(video_file=video_file),
                         tracking=dict(method=MouseTrackPipeline,
                                       estimator=SnoutPositionEstimator))

    def get_stim_sequence(self):
        return [PosTrackingStimulus(duration=120)]


if __name__ == "__main__":
    Stytra(protocol=RatProtocol())
