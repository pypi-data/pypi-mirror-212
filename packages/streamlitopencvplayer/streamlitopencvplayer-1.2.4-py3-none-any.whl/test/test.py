"""Test script."""

import argparse
import uuid

import streamlit as st

from streamlitopencvplayer.app import display_video

# Initiate all session states used
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0
if 'frames' not in st.session_state:
    st.session_state['frames'] = []


class opencvplayer:
    """Class streamlit opencv player."""

    def __init__(self, video_path, alerts_dict={}, alerts=[], data=[]):
        self.video_path = video_path
        self.alerts_dict = alerts_dict
        self.alerts = alerts
        self.data = data

    def main(self):
        """Test function.

        Args:
            video_path (required): video file path or video url.
            alerts_dict (Optional) : Dictionary of alerts passed to the alerts table.
            alerts (Required when data is used) : List of alerts time
            data (Optional) : bounding box coordinates, score and class
            This is an example for test :
                self.alerts_dict = {"Alerts": [43, 64]}
                self.alerts = [43, 64]
                self.data = [[[10, 100, 290, 200], 0.82, 0, "Class 0"],
                        [[55, 22, 100, 120], 0.9, 1, "Class 1"]]

        Returns:
            The video Player.
        """
        if self.video_path is not None:
            return display_video(self.video_path, self.alerts_dict, self.alerts, self.data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runnnig...")
    parser.add_argument(
        "--video-path",
        "-V",
        help="Enter the video path",
        default=str(uuid.uuid4().hex),
    )
    parser.add_argument("--alerts-dict",
                        "-T",
                        default={"Alerts": []},
                        help="Add alerts time to dict"
                        )
    parser.add_argument("--alerts",
                        "-A",
                        default=[],
                        type=list,
                        help="Add alerts time to list"
                        )

    parser.add_argument("--data",
                        "-D",
                        default=[],
                        type=list,
                        help="Add bounding box coordinates, score and class to list"
                        )
    args = parser.parse_args()
    opencvplayer = opencvplayer(
        args.video_path, args.alerts_dict, args.alerts, args.data)
    opencvplayer.main()
