import unittest

from scipy.signal import minimum_phase

from util.processing import *
from util.datamodel import *
from util.preparation import *
from pathlib import Path
from math import pi
import numpy as np
import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as pltticker
import matplotlib.colors as colors
from matplotlib.patches import Circle, Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import util.ScientificColourMaps5 as SCMaps

fontsize1, fontsize2, fontsize3, fontsize4 = [14, 10, 8, 6]
gray_light, gray_med, gray_heavy = ['#D0D0D0', '#808080', '#606060']
color_ideal, color_raw, color_filtered = [gray_med, '#FC0352', '#03A1FC']
color_vm, color_ca = ['#FF9999', '#99FF99']
# File paths  and files needed for tests
dir_cwd = Path.cwd()
dir_tests = str(dir_cwd)


def plot_test():
    fig = plt.figure(figsize=(8, 5))  # _ x _ inch page
    axis = fig.add_subplot(111)
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.tick_params(axis='x', which='minor', length=3, bottom=True)
    axis.tick_params(axis='x', which='major', length=8, bottom=True)
    plt.rc('xtick', labelsize=fontsize2)
    plt.rc('ytick', labelsize=fontsize2)
    return fig, axis


def plot_filter_spatial():
    # Setup a figure to show a noisy frame, a spatially filtered frame, and an ideal frame
    fig = plt.figure(figsize=(10, 5))  # _ x _ inch page
    axis_frame = fig.add_subplot(131)
    axis_filtered = fig.add_subplot(132)
    axis_ideal = fig.add_subplot(133)
    # Common between the two
    for ax in [axis_ideal, axis_frame, axis_filtered]:
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_xticklabels([])

    return fig, axis_frame, axis_filtered, axis_ideal


def plot_map():
    # Setup a figure to show a frame and a map generated from that frame
    fig = plt.figure(figsize=(8, 5))  # _ x _ inch page
    axis_img = fig.add_subplot(121)
    axis_map = fig.add_subplot(122)
    # Common between the two
    for ax in [axis_img, axis_map]:
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_yticks([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_xticklabels([])

    return fig, axis_img, axis_map


def plot_stats_bars(labels):
    fig = plt.figure(figsize=(8, 5))  # _ x _ inch page
    axis = fig.add_subplot(111)
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    ticks = []
    for i in range(0, len(labels)):
        x_tick = (1 / len(labels)) * i
        ticks.append(x_tick)
    axis.set_xticks(ticks)
    axis.set_xticklabels(labels, fontsize=9)
    axis.xaxis.set_ticks_position('bottom')
    axis.yaxis.set_ticks_position('left')
    plt.rc('xtick', labelsize=fontsize2)
    plt.rc('ytick', labelsize=fontsize2)
    return fig, axis


def plot_stats_scatter():
    fig = plt.figure(figsize=(8, 5))  # _ x _ inch page
    axis = fig.add_subplot(111)
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    plt.rc('xtick', labelsize=fontsize2)
    plt.rc('ytick', labelsize=fontsize2)
    return fig, axis


def run_trials_snr(self, trials_count, noise=0):
    # SNR Trials
    trials_snr = np.empty(trials_count)
    trials_peak_peak = np.empty(trials_count)
    trials_sd_noise = np.empty(trials_count)
    results = {'snr': {'array': trials_snr, 'mean': 0, 'sd': 0},
               'peak_peak': {'array': trials_peak_peak, 'mean': 0, 'sd': 0},
               'sd_noise': {'array': trials_sd_noise, 'mean': 0, 'sd': 0}}
    for trial in range(0, trials_count):
        time_ca, signal_ca = model_transients(model_type='Ca', t0=self.signal_t0, t=self.signal_time,
                                              f_0=self.signal_F0, f_amp=self.signal_amp, noise=noise)
        snr, rms_bounds, peak_peak, sd_noise, ir_noise, ir_peak \
            = calculate_snr(signal_ca, noise_count=self.noise_count)

        trials_snr[trial] = snr
        trials_peak_peak[trial] = peak_peak
        trials_sd_noise[trial] = sd_noise

    results['snr']['mean'] = np.mean(trials_snr)
    results['snr']['sd'] = statistics.stdev(trials_snr)
    results['peak_peak']['mean'] = np.mean(trials_peak_peak)
    results['peak_peak']['sd'] = statistics.stdev(trials_peak_peak)
    results['sd_noise']['mean'] = np.mean(trials_sd_noise)
    results['sd_noise']['sd'] = statistics.stdev(trials_sd_noise)
    return results


class TestFilterSpatial(unittest.TestCase):
    def setUp(self):
        # Setup data to test with, a propagating stack of varying SNR
        self.filter_type = 'gaussian'
        self.kernel = 5

        self.f_0 = 1000
        self.f_amp = 100
        self.noise = 5
        self.time_noisy_ca, self.stack_noisy_ca = model_stack_propagation(
            model_type='Ca', f_0=self.f_0, f_amp=self.f_amp, noise=self.noise)
        self.time_ideal_ca, self.stack_ideal_ca = model_stack_propagation(
            model_type='Ca', f_0=self.f_0, f_amp=self.f_amp)

        # Test temporal filtering on real signal data
        # File paths and files needed for the test
        file_name_rat = '201-/--/-- rat-04, PCL 240ms'
        file_stack_rat = dir_tests + '/data/20190320-04-240_tagged.tif'
        # file_name_pig = '2019/03/22 pigb-01, PCL 150ms'
        # file_signal_pig = dir_tests + '/data/20190322-pigb/01-350_Ca_15x15-LV-198x324.csv'
        self.file_name, self.file_stack = file_name_rat, file_stack_rat
        self.stack_real, self.stack_real_meta = open_stack(source=file_stack_rat)

        self.frame_num = int(len(self.stack_noisy_ca) / 8)  # frame from 1/8th total time
        self.frame_noisy_ca = self.stack_noisy_ca[self.frame_num]
        self.frame_ideal_ca = self.stack_ideal_ca[self.frame_num]
        self.stack_ca_shape = self.stack_noisy_ca.shape
        self.FRAMES = self.stack_noisy_ca.shape[0]
        self.HEIGHT, self.WIDTH = (self.stack_ca_shape[1], self.stack_ca_shape[2])
        self.frame_shape = (self.HEIGHT, self.WIDTH)
        self.origin_x, self.origin_y = self.WIDTH / 2, self.HEIGHT / 2

    def test_params(self):
        # Make sure type errors are raised when necessary
        # frame_in : ndarray, 2-D array
        frame_bad_shape = np.full(100, 100, dtype=np.uint16)
        frame_bad_type = np.full(self.stack_ca_shape, True)
        self.assertRaises(TypeError, filter_spatial, frame_in=True)
        self.assertRaises(TypeError, filter_spatial, frame_in=frame_bad_shape)
        self.assertRaises(TypeError, filter_spatial, frame_in=frame_bad_type)
        # filter_type : str
        self.assertRaises(TypeError, filter_spatial, frame_in=self.frame_noisy_ca, filter_type=True)
        # kernel : int
        self.assertRaises(TypeError, filter_spatial, frame_in=self.frame_noisy_ca, kernel=True)

        # Make sure parameters are valid, and valid errors are raised when necessary
        # filter_type : must be in FILTERS_SPATIAL
        self.assertRaises(ValueError, filter_spatial, frame_in=self.frame_noisy_ca, filter_type='gross')
        # kernel : >= 3, odd
        self.assertRaises(ValueError, filter_spatial, frame_in=self.frame_noisy_ca, kernel=2)
        self.assertRaises(ValueError, filter_spatial, frame_in=self.frame_noisy_ca, kernel=8)

    def test_results(self):
        # Make sure spatial filter results are correct
        frame_out = filter_spatial(self.frame_noisy_ca)
        # frame_out : ndarray
        self.assertIsInstance(frame_out, np.ndarray)  # frame_out type
        self.assertEqual(frame_out.shape, self.frame_shape)  # frame_out shape
        self.assertIsInstance(frame_out[0, 0], type(self.frame_noisy_ca[0, 0]))  # frame_out value type same as input

    def test_plot(self):
        # Make sure filtered frame looks correct
        frame_out = filter_spatial(self.frame_noisy_ca, filter_type=self.filter_type)

        # Plot a frame from the stack and the filtered frame
        fig_filtered, ax_noisy, ax_filtered, ax_ideal = plot_filter_spatial()
        # Create normalization colormap range for all frames (round up to nearest 10)
        cmap_frames = SCMaps.grayC.reversed()
        frames_min, frames_max = 0, 0
        for frame in [self.frame_noisy_ca, frame_out, self.frame_ideal_ca]:
            frames_min = min(frames_max, np.nanmin(frame))
            frames_max = max(frames_max, np.nanmax(frame))
        cmap_norm = colors.Normalize(vmin=round(frames_min, -1),
                                     vmax=round(frames_max + 5.1, -1))
        # Noise frame
        ax_noisy.set_title('Noisy Model Data\n(noise SD: {})'.format(self.noise))
        img_noisy = ax_noisy.imshow(self.frame_noisy_ca, cmap=cmap_frames, norm=cmap_norm)
        # Draw shape and size of spatial filter kernel

        # Filtered frame
        ax_filtered.set_title('Spatially Filtered\n({}, kernel: {})'.format(self.filter_type, self.kernel))
        img_filtered = ax_filtered.imshow(frame_out, cmap=cmap_frames, norm=cmap_norm)

        # Ideal frame
        ax_ideal.set_title('Model Data')
        img_ideal = ax_ideal.imshow(self.frame_ideal_ca, cmap=cmap_frames, norm=cmap_norm)
        # Add colorbar (right of frame)
        ax_ins_filtered = inset_axes(ax_ideal, width="5%", height="80%", loc=5, bbox_to_anchor=(0.1, 0, 1, 1),
                                     bbox_transform=ax_ideal.transAxes, borderpad=0)
        cb_filtered = plt.colorbar(img_ideal, cax=ax_ins_filtered, orientation="vertical")
        cb_filtered.ax.set_xlabel('a.u.', fontsize=fontsize3)
        cb_filtered.ax.yaxis.set_major_locator(pltticker.LinearLocator(2))
        cb_filtered.ax.yaxis.set_minor_locator(pltticker.LinearLocator(10))
        cb_filtered.ax.tick_params(labelsize=fontsize3)

        fig_filtered.show()

    def test_plot_trace(self):
        # Make sure filtered stack signals looks correct
        signal_x, signal_y = (int(self.WIDTH / 3), int(self.HEIGHT / 3))
        signal_r = self.kernel / 2
        # Filter a noisy stack
        stack_filtered = np.empty_like(self.stack_noisy_ca)
        for idx, frame in enumerate(self.stack_noisy_ca):
            f_filtered = filter_spatial(frame, filter_type=self.filter_type)
            stack_filtered[idx, :, :] = f_filtered
        frame_filtered = stack_filtered[self.frame_num]

        # General layout
        fig_filter_traces = plt.figure(figsize=(8, 6))  # _ x _ inch page
        gs0 = fig_filter_traces.add_gridspec(1, 3)  # 1 row, 3 columns
        titles = ['Noisy Model Data\n(noise SD: {})'.format(self.noise),
                  'Spatially Filtered\n({}, kernel: {})'.format(self.filter_type, self.kernel),
                  'Model Data']
        # Create normalization colormap range for all frames (round up to nearest 10)
        cmap_frames = SCMaps.grayC.reversed()
        frames_min, frames_max = 0, 0
        for idx, frame in enumerate([self.frame_noisy_ca, frame_filtered, self.frame_ideal_ca]):
            frames_min = min(frames_max, np.nanmin(frame))
            frames_max = max(frames_max, np.nanmax(frame))
            cmap_norm = colors.Normalize(vmin=round(frames_min, -1),
                                         vmax=round(frames_max + 5.1, -1))

        # Plot the frame and a trace from the stack
        for idx, stack in enumerate([self.stack_noisy_ca, stack_filtered, self.stack_ideal_ca]):
            frame = stack[self.frame_num]
            signal = stack[:, signal_y, signal_x]
            gs_frame_signal = gs0[idx].subgridspec(2, 1, height_ratios=[0.6, 0.4])  # 2 rows, 1 columns
            ax_frame = fig_filter_traces.add_subplot(gs_frame_signal[0])
            # Frame image
            ax_frame.set_title(titles[idx], fontsize=fontsize2)
            img_frame = ax_frame.imshow(frame, cmap=cmap_frames, norm=cmap_norm)
            ax_frame.set_yticks([])
            ax_frame.set_yticklabels([])
            ax_frame.set_xticks([])
            ax_frame.set_xticklabels([])
            frame_signal_rect = Rectangle((signal_x - signal_r, signal_y - signal_r),
                                          width=signal_r * 2, height=signal_r * 2,
                                          fc=gray_med, ec=gray_heavy, lw=1, linestyle='--')
            ax_frame.add_artist(frame_signal_rect)
            if idx is len(titles) - 1:
                # Add colorbar (right of frame)
                ax_ins_filtered = inset_axes(ax_frame, width="5%", height="80%", loc=5, bbox_to_anchor=(0.15, 0, 1, 1),
                                             bbox_transform=ax_frame.transAxes, borderpad=0)
                cb_filtered = plt.colorbar(img_frame, cax=ax_ins_filtered, orientation="vertical")
                cb_filtered.ax.set_xlabel('a.u.', fontsize=fontsize3)
                cb_filtered.ax.yaxis.set_major_locator(pltticker.LinearLocator(2))
                cb_filtered.ax.yaxis.set_minor_locator(pltticker.LinearLocator(10))
                cb_filtered.ax.tick_params(labelsize=fontsize3)
            # Signal trace
            ax_signal = fig_filter_traces.add_subplot(gs_frame_signal[1])
            ax_signal.set_xlabel('Time (ms)')
            ax_signal.set_yticks([])
            ax_signal.set_yticklabels([])
            # Common between the two
            for ax in [ax_frame, ax_signal]:
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
            ax_signal.plot(self.time_noisy_ca, signal, color=gray_heavy, linestyle='None', marker='+')

        fig_filter_traces.show()
        fig_filter_traces.savefig(dir_tests + '/results/processing_SpatialFilterTraces_ca.png')

    def test_plot_trace_real(self):
        # Make sure filtered stack signals looks correct
        fps = 800
        frame_num = int(len(self.stack_real) / 8)  # frame from 1/8th total time
        frame_real = self.stack_real[frame_num]
        # self.frame_ideal_ca = self.stack_ideal_ca[self.frame_num]
        stack_shape = self.stack_real.shape
        FRAMES = self.stack_real.shape[0]
        HEIGHT, WIDTH = (self.stack_real.shape[1], self.stack_real.shape[2])
        frame_shape = (HEIGHT, WIDTH)
        origin_x, origin_y = WIDTH / 2, HEIGHT / 2

        signal_x, signal_y = (int(WIDTH / 3), int(HEIGHT / 3))
        signal_r = self.kernel / 2
        # Filter a noisy real stack
        stack_filtered = np.empty_like(self.stack_real)
        for idx, frame in enumerate(self.stack_real):
            f_filtered = filter_spatial(frame, filter_type=self.filter_type)
            stack_filtered[idx, :, :] = f_filtered
        frame_filtered = stack_filtered[frame_num]

        # General layout
        fig_filter_traces = plt.figure(figsize=(8, 6))  # _ x _ inch page
        gs0 = fig_filter_traces.add_gridspec(1, 2)  # 1 row, 2 columns
        titles = ['Real Data\n({})'.format(self.file_name),
                  'Spatially Filtered\n({}, kernel: {})'.format(self.filter_type, self.kernel)]
        # Create normalization colormap range for all frames (round up to nearest 10)
        cmap_frames = SCMaps.grayC.reversed()
        frames_min, frames_max = 0, 0
        for idx, frame in enumerate([frame_real, frame_filtered]):
            frames_min = min(frames_max, np.nanmin(frame))
            frames_max = max(frames_max, np.nanmax(frame))
            cmap_norm = colors.Normalize(vmin=round(frames_min, -1),
                                         vmax=round(frames_max + 5.1, -1))

        # Plot the frame and a trace from the stack
        for idx, stack in enumerate([self.stack_real, stack_filtered]):
            frame = stack[frame_num]
            # Generate array of timestamps
            FPMS = fps / 1000
            FRAME_T = 1 / FPMS
            FINAL_T = floor(FPMS * FRAMES)
            signal_time = np.linspace(start=0, stop=FINAL_T, num=FRAMES)
            signal = stack[:, signal_y, signal_x]
            gs_frame_signal = gs0[idx].subgridspec(2, 1, height_ratios=[0.6, 0.4])  # 2 rows, 1 columns
            ax_frame = fig_filter_traces.add_subplot(gs_frame_signal[0])
            # Frame image
            ax_frame.set_title(titles[idx], fontsize=fontsize2)
            img_frame = ax_frame.imshow(frame, cmap=cmap_frames, norm=cmap_norm)
            ax_frame.set_yticks([])
            ax_frame.set_yticklabels([])
            ax_frame.set_xticks([])
            ax_frame.set_xticklabels([])
            frame_signal_rect = Rectangle((signal_x - signal_r, signal_y - signal_r),
                                          width=signal_r * 2, height=signal_r * 2,
                                          fc=gray_med, ec=gray_heavy, lw=1, linestyle='--')
            ax_frame.add_artist(frame_signal_rect)
            if idx is len(titles) - 1:
                # Add colorbar (right of frame)
                ax_ins_filtered = inset_axes(ax_frame, width="5%", height="80%", loc=5, bbox_to_anchor=(0.15, 0, 1, 1),
                                             bbox_transform=ax_frame.transAxes, borderpad=0)
                cb_filtered = plt.colorbar(img_frame, cax=ax_ins_filtered, orientation="vertical")
                cb_filtered.ax.set_xlabel('a.u.', fontsize=fontsize3)
                cb_filtered.ax.yaxis.set_major_locator(pltticker.LinearLocator(2))
                cb_filtered.ax.yaxis.set_minor_locator(pltticker.LinearLocator(10))
                cb_filtered.ax.tick_params(labelsize=fontsize3)
            # Signal trace
            ax_signal = fig_filter_traces.add_subplot(gs_frame_signal[1])
            ax_signal.set_xlabel('Time (ms)')
            ax_signal.set_yticks([])
            ax_signal.set_yticklabels([])
            # Common between the two
            for ax in [ax_frame, ax_signal]:
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
            ax_signal.plot(signal_time, signal, color=gray_heavy, linestyle='None', marker='+')

        fig_filter_traces.savefig(dir_tests + '/results/processing_SpatialFilter_Real.png')
        fig_filter_traces.show()

    def test_plot_all(self):
        # Plot all filters to compare
        # Setup a figure to show a noisy frame, a spatially filtered frames, and an ideal frame
        fig_filters = plt.figure(figsize=(8, 12))  # _ x _ inch page
        # General layout
        gs0 = fig_filters.add_gridspec(2, 1)  # 2 rows, 1 column
        gs_frames = gs0[1].subgridspec(1, 2)  # 1 row, 2 columns
        # Create normalization colormap range for the frames (round up to nearest 10)
        cmap_frames = SCMaps.grayC.reversed()
        frames_min, frames_max = 0, 0
        for frame in [self.frame_ideal_ca, self.frame_noisy_ca]:
            frames_min = min(frames_max, np.nanmin(frame))
            frames_max = max(frames_max, np.nanmax(frame))
        cmap_norm = colors.Normalize(vmin=round(frames_min, -1),
                                     vmax=round(frames_max + 5.1, -1))

        # Noisy frame
        ax_noisy = fig_filters.add_subplot(gs_frames[0])
        ax_noisy.set_title('Noisy Model Data\n(noise SD: {})'.format(self.noise))
        img_noisy = ax_noisy.imshow(self.frame_noisy_ca, cmap=cmap_frames, norm=cmap_norm)

        # Filtered frames
        gs_filters = gs0[0].subgridspec(1, len(FILTERS_SPATIAL))  # 1 row, X columns
        # Common between the two
        for idx, filter_type in enumerate(FILTERS_SPATIAL):
            filtered_ca = filter_spatial(self.frame_noisy_ca, filter_type=filter_type)
            ax = fig_filters.add_subplot(gs_filters[idx])
            ax.set_title('{}, kernel: {}'.format(filter_type, self.kernel))
            img_filter = ax.imshow(filtered_ca, cmap=cmap_frames, norm=cmap_norm)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.set_xticklabels([])

        # Ideal frame
        ax_ideal = fig_filters.add_subplot(gs_frames[1])
        ax_ideal.set_title('Model Data')
        img_ideal = ax_ideal.imshow(self.frame_ideal_ca, cmap=cmap_frames, norm=cmap_norm)
        # Add colorbar (right of frame)
        ax_cb = inset_axes(ax_ideal, width="5%", height="80%", loc=5, bbox_to_anchor=(0.1, 0, 1, 1),
                           bbox_transform=ax_ideal.transAxes, borderpad=0)
        cb_filtered = plt.colorbar(img_filter, cax=ax_cb, orientation="vertical")
        cb_filtered.ax.set_xlabel('a.u.', fontsize=fontsize3)
        cb_filtered.ax.yaxis.set_major_locator(pltticker.LinearLocator(2))
        cb_filtered.ax.yaxis.set_minor_locator(pltticker.LinearLocator(10))
        cb_filtered.ax.tick_params(labelsize=fontsize3)

        for ax in [ax_noisy, ax_ideal]:
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.set_yticks([])
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.set_xticklabels([])
        fig_filters.show()
        fig_filters.savefig(dir_tests + '/results/processing_SpatialFilters_ca.png')


class TestFilterTemporal(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.t = 200
        self.t0 = 50
        self.fps = 1000
        self.signal_F0 = 200
        self.signal_amp = 100
        self.noise = 5
        self.time_noisy_ca, self.signal_noisy_ca = model_transients(model_type='Ca', t=self.t, t0=self.t0, fps=self.fps,
                                                                    f_0=self.signal_F0, f_amp=self.signal_amp,
                                                                    noise=self.noise)
        self.time_ideal_ca, self.signal_ideal_ca = model_transients(model_type='Ca', t=self.t, t0=self.t0, fps=self.fps,
                                                                    f_0=self.signal_F0, f_amp=self.signal_amp)
        self.sample_rate = float(self.fps)

    def test_params(self):
        signal_bad_type = np.full(100, True)
        # Make sure type errors are raised when necessary
        # signal_in : ndarray, dtyoe : uint16 or float
        self.assertRaises(TypeError, filter_temporal, signal_in=True, sample_rate=self.sample_rate)
        self.assertRaises(TypeError, filter_temporal, signal_in=signal_bad_type, sample_rate=self.sample_rate)
        # sample_rate : float
        self.assertRaises(TypeError, filter_temporal, signal_in=self.signal_noisy_ca, sample_rate=True)
        # freq_cutoff : float
        self.assertRaises(TypeError, filter_temporal, signal_in=self.signal_noisy_ca, freq_cutoff=True)
        # filter_order : int or 'auto'
        self.assertRaises(TypeError, filter_temporal, signal_in=self.signal_noisy_ca, sample_rate=self.sample_rate,
                          filter_order=True)

        # Make sure parameters are valid, and valid errors are raised when necessary
        # filter_order : if a str, must be 'auto'
        self.assertRaises(ValueError, filter_temporal, signal_in=self.signal_noisy_ca, sample_rate=self.sample_rate,
                          filter_order='gross')

    def test_results(self):
        # Make sure results are correct
        signal_out = filter_temporal(self.signal_noisy_ca, self.sample_rate)

        # signal_out : ndarray
        self.assertIsInstance(signal_out, np.ndarray)  # filtered signal

        # Make sure result values are valid
        # self.assertAlmostEqual(signal_out.min(), self.signal_ideal_ca.min(), delta=20)
        # self.assertAlmostEqual(signal_out.max(), self.signal_ideal_ca.max(), delta=20)

    def test_plot_filter(self):
        # Plot filter frequency response(s)
        f_cutoff = 100.0  # Cutoff frequency of the lowpass filter
        # The Nyquist rate of the signal.
        nyq_rate = self.sample_rate / 2.0

        # # Butterworth (from old code)
        # window = 'IIR Butterworth'
        # n_order = 10
        # Wn = f_cutoff / nyq_rate
        # [b, a] = butter(n_order, Wn)
        # w, h = freqz(b, a)   # for FIR, a=1
        # # signal_out = filtfilt(b, a, signal_in)

        # FIR
        # # FIR 1 design arguements
        # window = 'remez'
        # # window = 'remez, hilbert'
        # Fs = self.sample_rate           # sample-rate, down-sampled
        # # taps = 2 ** 2
        # n_order = 200
        # Ntaps = n_order + 1   # The desired number of taps in the filter
        # Fpass = 95       # passband edge
        # Fstop = 105     # stopband edge, transition band 100kHz
        # Wp = Fpass/Fs    # pass normalized frequency
        # Ws = Fstop/Fs    # stop normalized frequency
        # taps = ffd.remez(Ntaps, [0, Wp, Ws, .5], [1, 0], maxiter=10000)
        # # taps = minimum_phase(taps, method='hilbert')

        # # FIR 2 design    - https://scipy-cookbook.readthedocs.io/items/FIRFilter.html
        # # The desired width of the transition from pass to stop,
        # # relative to the Nyquist rate.  We'll design the filter
        # # with a 5 Hz transition width.
        # width = 10 / nyq_rate
        # # The desired attenuation in the stop band, in dB.
        # ripple_db = 60.0
        # # Compute the order and Kaiser parameter for the FIR filter.
        # n_order, beta = kaiserord(ripple_db, width)
        # # Use firwin with a Kaiser window to create a lowpass FIR filter.
        # window = 'kaiser'
        # taps = firwin(n_order, cutoff=f_cutoff, window=(window, beta), fs=self.sample_rate)
        # # # Calculate frequency response
        # w, h = freqz(taps)

        # # FIR 3 design  - http://pyageng.mpastell.com/book/dsp.html
        # n_order = 100
        # window = 'hamming'
        # # Design filter
        # taps = firwin(n_order, cutoff=f_cutoff, window=window, fs=self.sample_rate)

        # FIR 4 design  - https://www.programcreek.com/python/example/100540/scipy.signal.firwin
        # Compute the order and Kaiser parameter for the FIR filter.
        ripple_db = 30.0
        width = 20  # The desired width of the transition from pass to stop, Hz
        window = 'kaiser'
        n_order, beta = kaiserord(ripple_db, width / nyq_rate)
        # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(numtaps=n_order + 1, cutoff=f_cutoff, window=(window, beta), fs=self.sample_rate)
        # the filter must be symmetric, in order to be zero-phase
        assert np.all(np.abs(taps - taps[::-1]) < 1e-15)
        # filtfilt(b, a, sig, method="gust")
        # Calculate frequency response (magnitude and phase)
        w, h = freqz(taps)  # for FIR, a=1

        # # # FIR 5 design
        # window = 'hamming'
        # n_order = 150
        # taps = firwin2(n_order, [0.0, 0.5, 1.0], [1.0, 1.0, 0.0], window=window, fs=self.sample_rate)
        # # Calculate frequency response (magnitude and phase)
        # w, h = freqz(taps, 1)   # for FIR, a=1

        phase_delay = 0.5 * (n_order - 1) / self.sample_rate
        h_phase = np.unwrap(np.arctan2(np.imag(h), np.real(h)))
        df_h_phase = np.diff(h_phase, n=1, prepend=int(h_phase[0])).astype(float)
        print('phase_delay : {} '.format(phase_delay))
        print('Delay (slope) : {} '.format(df_h_phase[1]))

        # Build figure
        fig_filter, ax_mag = plot_test()
        ax_mag.spines['top'].set_visible(False)
        # Magnitude
        # ax_mag.set_title('Butterworth filter frequency response\n(Analog, n = {}))'.format(n_order))
        ax_mag.set_title('Custom FIR filter frequency response\n({}, n={}, phase delay={} s)'
                         .format(window, n_order, phase_delay))
        # ax_mag.set_xlabel('Frequency [radians / second]')
        ax_mag.set_xlabel('Frequency (Hz)')
        ax_mag.set_xlim(0, 500)
        ax_mag.set_ylabel('Magnitude (dB)', color=color_filtered)
        ax_mag.set_ylim(-150, 10)
        ax_mag.grid(which='both', axis='both')

        # ax_mag.plot(w / (2 * pi), 20 * np.log10(abs(h)), color=color_filtered) # analog or butterworth?
        ax_mag.plot((w / pi) * nyq_rate, 20 * np.log10(abs(h)), color=color_filtered, label='Magnitude')
        ax_mag.axvline(f_cutoff, color='green')  # cutoff frequency

        # Phase
        ax_phase = ax_mag.twinx()  # instantiate a second axes that shares the same x-axis
        ax_phase.spines['top'].set_visible(False)
        # ax_phase.set_xlabel('Normalized frequency (1.0 = Nyquist)')
        ax_phase.set_ylabel('Phase (rad.)')
        # ax_phase.set_ylim(-150, 10)
        ax_phase.set_yticks([-np.pi, -0.5 * np.pi, 0, 0.5 * np.pi, np.pi])
        ax_phase.set_yticklabels([r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])

        # ax_phase.plot(w / (2 * pi), np.angle(h, deg=True), color=gray_med, linestyle='--')
        ax_phase.plot((w / pi) * nyq_rate, np.angle(h), color=gray_med, linestyle='--', label='Phase')
        # ax_phase.plot((w/pi) * nyq_rate, h_phase, color=gray_med, linestyle='--')

        # h_phase_corrected = h_phase * (phase_delay / (2*pi))
        # h_phase_corrected = h_phase / df_h_phase
        # ax_phase.plot((w/pi) * nyq_rate, h_phase_corrected, color=gray_med, linestyle=':')
        # ax_mag.legend(loc='lower left', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        # ax_phase.legend(loc='lower right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        fig_filter.show()

    def test_plot_error(self):
        # Make sure filtered signal looks correct
        ideal_norm = normalize_signal(self.signal_ideal_ca)
        noisy_norm = normalize_signal(self.signal_noisy_ca)
        freq_cutoff = 100.0
        filter_order = 'auto'
        signal_filtered = filter_temporal(self.signal_noisy_ca, self.sample_rate, freq_cutoff=freq_cutoff,
                                          filter_order=filter_order)
        filtered_norm = normalize_signal(signal_filtered)

        fig_filter, ax_filter = plot_test()
        ax_filter.set_title('Temporal Filtering\n'
                            '(noise SD: {}, {} Hz lowpass, filter order: {})'.format(self.noise, freq_cutoff, filter_order))
        ax_filter.set_ylabel('Arbitrary Fluorescent Units')
        ax_filter.set_xlabel('Time (ms)')
        # ax_filter.set_ylim([self.signal_F0 - 20, self.signal_F0 + self.signal_amp + 20])

        ax_filter.plot(self.time_noisy_ca, self.signal_ideal_ca, color=color_ideal, linestyle='None', marker='+',
                       label='Ca (Model)')
        ax_filter.plot(self.time_noisy_ca, self.signal_noisy_ca, color=color_raw, linestyle='None', marker='+',
                       label='Ca (w/ noise)')
        ax_filter.plot(self.time_noisy_ca, signal_filtered,
                       color=color_filtered, linestyle='None', marker='+',
                       label='Ca (Filtered)')

        # ideal_norm_align = ideal_norm[filter_order - 1:]
        error, error_mean, error_sd = calculate_error(self.signal_ideal_ca, signal_filtered)
        ax_error = ax_filter.twinx()  # instantiate a second axes that shares the same x-axis
        ax_error.baseline = ax_error.axhline(color=gray_light, linestyle='-.')
        ax_error.set_ylabel('% Error')  # we already handled the x-label with ax1
        ax_error.set_ylim([-10, 10])
        ax_error.plot(self.time_noisy_ca, error,
                      color=gray_heavy, linestyle='-', label='% Error')

        ax_filter.legend(loc='upper left', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        ax_error.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_filter.savefig(dir_tests + '/results/processing_TemporalFilterTraces.png')
        fig_filter.show()

    def test_plot_real(self):
        # Test temporal filtering on real signal data
        # File paths and files needed for the test
        file_name_rat = '2019/04/04 rata-12-Ca, PCL 150ms'
        file_signal_rat = dir_tests + '/data/20190404-rata-12-150_right_signal1.csv'
        file_name_pig = '2019/03/22 pigb-01-Ca, PCL 150ms'
        file_signal_pig = dir_tests + '/data/20190322-pigb/01-350_Ca_15x15-LV-198x324.csv'
        file_name, file_signal = file_name_rat, file_signal_rat
        time, signal = open_signal(source=file_signal)

        freq_cutoff = 100.0
        filter_order = 20
        signal_filtered = filter_temporal(signal, sample_rate=800.0, freq_cutoff=freq_cutoff, filter_order=filter_order)

        fig_filter, ax_filter = plot_test()
        ax_filter.set_title('Single=pixel Temporal Filtering\n({} Hz lowpass, n={})'.format(freq_cutoff, filter_order))
        ax_filter.text(0.65, -0.12, file_name,
                       color=gray_med, fontsize=fontsize2, transform=ax_filter.transAxes)

        ax_filter.set_ylabel('Arbitrary Fluorescent Units')
        ax_filter.set_xlabel('Time (ms)')

        ax_filter.plot(time, signal, color=color_raw, linestyle='None', marker='+',
                       label='Ca')
        ax_filter.plot(time, signal_filtered,
                       color=color_filtered, linestyle='None', marker='+',
                       label='Ca (Filtered)')

        ax_filter.legend(loc='upper left', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_filter.savefig(dir_tests + '/results/processing_TemporalFilter_Real.png')
        fig_filter.show()


class TestFilterDrift(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.t = 500
        self.t0 = 200
        self.fps = 1000
        self.signal_F0 = 1000
        self.signal_amp = 100
        self.noise = 3
        self.time_noisy_ca, self.signal_noisy_ca = model_transients(model_type='Ca', t=self.t, t0=self.t0, fps=self.fps,
                                                                    f_0=self.signal_F0, f_amp=self.signal_amp,
                                                                    noise=self.noise)
        self.time_ideal_ca, self.signal_ideal_ca = model_transients(model_type='Ca', t=self.t, t0=self.t0, fps=self.fps,
                                                                    f_0=self.signal_F0, f_amp=self.signal_amp)
        self.time, self.signal_ideal = self.time_noisy_ca, self.signal_noisy_ca

        # # Polynomial drift
        # poly_ideal_order = 1
        # poly_ideal_splope = -0.5
        # poly_ideal = np.poly1d([poly_ideal_splope, signal_F0 - (poly_ideal_splope * t)])  # linear, decreasing
        # drift_ideal_y = poly_ideal(time)
        # drift_ideal_d = drift_ideal_y - drift_ideal_y.min()
        # Exponential drift
        self.poly_ideal_order = 'exp'
        exp_b = 0.03
        self.exp_ideal = self.signal_amp * np.exp(-exp_b * self.time) + self.signal_F0
        self.drift_ideal_y = self.exp_ideal
        drift_ideal_d = self.drift_ideal_y - self.drift_ideal_y.min()

        self.signal_drift = (self.signal_ideal + drift_ideal_d).astype(np.uint16)

    def test_params(self):
        signal_bad_type = np.full(100, True)
        # Make sure type errors are raised when necessary
        # signal_in : ndarray, dtyoe : uint16 or float
        self.assertRaises(TypeError, filter_drift, signal_in=True)
        self.assertRaises(TypeError, filter_drift, signal_in=signal_bad_type)
        # drift_order : int or 'str'
        self.assertRaises(TypeError, filter_drift, signal_in=self.signal_drift, drift_order=True)

        # Make sure parameters are valid, and valid errors are raised when necessary
        # poly_order : >= 1, <= 5
        self.assertRaises(ValueError, filter_drift, signal_in=self.signal_drift, drift_order=0)
        self.assertRaises(ValueError, filter_drift, signal_in=self.signal_drift, drift_order=6)
        # poly_order : if a str, must be 'exp'
        self.assertRaises(ValueError, filter_drift, signal_in=self.signal_drift, drift_order='gross')

    def test_results(self):
        # Make sure results are correct
        signal_out, drift = filter_drift(self.signal_drift, drift_order=self.poly_ideal_order)

        # signal_out : ndarray
        self.assertIsInstance(signal_out, np.ndarray)
        # signal_out.dtype : signal_in.dtype
        self.assertIsInstance(signal_out[1], type(self.signal_drift[1]))
        # drift : ndarray
        self.assertIsInstance(drift, np.ndarray)

        # Make sure result values are valid
        # self.assertAlmostEqual(signal_out.min(), self.signal_ideal_ca.min(), delta=self.noise * 4)  #
        # self.assertAlmostEqual(signal_out.max(), self.signal_ideal_ca.max(), delta=self.noise * 4)  #

    def test_plot_error(self):
        # Make sure drift calculations looks correct
        signal_filtered, drift = filter_drift(self.signal_drift, drift_order=self.poly_ideal_order)

        # Build a figure to plot new signal
        fig_drift, ax_drift = plot_test()
        ax_drift.set_title('Filter - Drift Removal\n'
                           '(noise SD: {}, polynomial order: {})'.format(self.noise, self.poly_ideal_order))
        ax_drift.set_ylabel('Arbitrary Fluorescent Units')
        ax_drift.set_xlabel('Time (ms)')

        ax_drift.plot(self.time, self.signal_ideal, color=color_ideal, linestyle='None', marker='+',
                      label='Ca - (Model)')
        ax_drift.plot(self.time, self.drift_ideal_y, color=gray_light, linestyle='None', marker='+',
                      label='Drift - (Model)')
        ax_drift.plot(self.time, self.signal_drift, color=color_raw, linestyle='None', marker='+',
                      label='Ca (w/ drift)')

        ax_drift.plot(self.time, drift, color=gray_med, linestyle='None', marker='+',
                      label='Drift (Calc.)')
        ax_drift.plot(self.time, signal_filtered, color=color_filtered, linestyle='None', marker='+',
                      label='Ca (Filtered)')

        error, error_mean, error_sd = calculate_error(self.signal_ideal, signal_filtered)
        ax_error = ax_drift.twinx()  # instantiate a second axes that shares the same x-axis
        ax_error.set_ylabel('% Error')  # we already handled the x-label with ax1
        ax_error.yaxis.set_major_locator(pltticker.MultipleLocator(5))
        ax_error.set_ylim([-10, 10])
        ax_error.baseline = ax_error.axhline(color=gray_light, linestyle='-.')
        ax_error.plot(self.time_noisy_ca, error,
                      color=gray_heavy, linestyle='-', label='% Error')

        ax_drift.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        ax_error.legend(loc='lower right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        fig_drift.show()
        fig_drift.savefig(dir_tests + '/results/processing_DriftFilterTraces.png')


class TestInvert(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.signal_F0 = 1000
        self.signal_amp = 100
        self.signal_t0 = 50
        self.signal_time = 1000
        self.signal_num = 5
        self.noise = 2  # as a % of the signal amplitude
        self.noise_count = 100
        self.time_vm, self.signal_vm = model_transients(t0=self.signal_t0, t=self.signal_time,
                                                        f_0=self.signal_F0, f_amp=self.signal_amp,
                                                        noise=self.noise, num=self.signal_num)

        # time_ca, signal_noisy_ca = model_transients(model_type='Ca', t0=signal_t0 + 15, t=signal_time,
        #                                       f_0=signal_F0, f_amp=signal_amp,
        #                                       noise=noise, num=signal_num)

    def test_params(self):
        signal_bad_type = np.full(100, True)
        # Make sure type errors are raised when necessary
        # signal_in : ndarray, dtyoe : uint16 or float
        self.assertRaises(TypeError, invert_signal, signal_in=True)
        self.assertRaises(TypeError, invert_signal, signal_in=signal_bad_type)

        # Make sure parameters are valid, and valid errors are raised when necessary

    def test_results(self):
        # Make sure results are correct
        signal_out = invert_signal(self.signal_vm)

        # signal_out : ndarray
        self.assertIsInstance(signal_out, np.ndarray)  # inverted signal

        # Make sure result values are valid
        self.assertAlmostEqual(signal_out.min(), self.signal_F0 - self.signal_amp, delta=self.noise * 4)  #
        self.assertAlmostEqual(signal_out.max(), self.signal_F0, delta=self.noise * 4)  #

    def test_plot_single(self):
        # Make sure signal inversion looks correct
        signal_out = invert_signal(self.signal_vm)

        # Build a figure to plot new signal
        fig_inv, ax_inv = plot_test()
        ax_inv.set_title('Signal Inversion')
        ax_inv.set_ylabel('Arbitrary Fluorescent Units')
        ax_inv.set_xlabel('Time (ms)')

        ax_inv.plot(self.time_vm, self.signal_vm, color=gray_light, linestyle='None', marker='+',
                    label='Vm')
        ax_inv.plot_vm_mean = ax_inv.axhline(y=self.signal_vm.mean(), color=gray_med, linestyle='-.')

        ax_inv.plot(self.time_vm, signal_out, color=gray_med, linestyle='None', marker='+',
                    label='Vm, Inverted')
        ax_inv.plot_vm_inv_mean = ax_inv.axhline(y=signal_out.mean(), color=gray_med, linestyle='-.')

        ax_inv.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_inv.savefig(dir_tests + '/results/processing_Inversion.png')
        fig_inv.show()


class TestNormalize(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.signal_F0 = 1000
        self.signal_amp = 100
        self.signal_t0 = 20
        self.signal_time = 500
        self.noise = 5  # as a % of the signal amplitude
        self.noise_count = 100
        self.time_ca, self.signal_ca = model_transients(model_type='Ca', t0=self.signal_t0, t=self.signal_time,
                                                        f_0=self.signal_F0, f_amp=self.signal_amp, noise=self.noise)

    def test_params(self):
        signal_bad_type = np.full(100, True)
        # Make sure type errors are raised when necessary
        # signal_in : ndarray, dtyoe : uint16 or float
        self.assertRaises(TypeError, normalize_signal, signal_in=True)
        self.assertRaises(TypeError, normalize_signal, signal_in=signal_bad_type)

        # Make sure parameters are valid, and valid errors are raised when necessary

    def test_results(self):
        # Make sure results are correct
        signal_out = normalize_signal(self.signal_ca)

        # signal_out : ndarray, dtyoe : float
        self.assertIsInstance(signal_out, np.ndarray)  # normalized signal

    def test_plot_single(self):
        # Make sure signal normalization looks correct
        signal_out = normalize_signal(self.signal_ca)

        # Build a figure to plot new signal
        fig_norm, ax_norm = plot_test()
        ax_norm.set_title('Signal Normalization')
        ax_norm.set_ylabel('Arbitrary Fluorescent Units')
        ax_norm.set_xlabel('Time (ms)')

        ax_norm.plot(self.time_ca, signal_out, color=gray_light, linestyle='None', marker='+',
                     label='Ca, Normalized')

        ax_norm.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_norm.savefig(dir_tests + '/results/processing_Normalization_ca.png')
        fig_norm.show()


class TestFF0(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.signal_F0 = 1000
        self.signal_amp = 100
        self.signal_t0 = 50
        self.signal_time = 500
        self.signal_num = 'full'
        self.signal_cl = 100
        self.noise = 2  # as a % of the signal amplitude
        self.noise_count = 100
        self.time_vm, self.signal_vm = model_transients(t0=self.signal_t0, t=self.signal_time,
                                                        f_0=self.signal_F0, f_amp=self.signal_amp,
                                                        noise=self.noise, num=self.signal_num, cl=self.signal_cl)
        self.time_ca, self.signal_ca = model_transients(model_type='Ca', t0=self.signal_t0 + 15, t=self.signal_time,
                                                        f_0=self.signal_F0, f_amp=self.signal_amp,
                                                        noise=self.noise, num=self.signal_num, cl=self.signal_cl)

    def test_parameters(self):
        # Make sure type errors are raised when necessary
        signal_bad_type = np.full(100, True)
        # signal_in : ndarray
        self.assertRaises(TypeError, calc_ff0, signal_in=True)
        self.assertRaises(TypeError, calc_ff0, signal_in=signal_bad_type)

        # Make sure parameters are valid, and valid errors are raised when necessary

    def test_results(self):
        # Make sure result types are valid
        signal_vm_ff0 = calc_ff0(self.signal_vm)
        signal_ca_ff0 = calc_ff0(self.signal_ca)
        # signal_out : ndarray, dtyoe : float
        self.assertIsInstance(signal_ca_ff0, np.ndarray)  # The array of F/F0 fluorescence data
        self.assertIsInstance(signal_ca_ff0[0], float)  # dtyoe : float

        # Make sure result values are valid
        # self.assertAlmostEqual(signal_ca_ff0.min(), signal_vm_ff0.max(), delta=0.01)  # Vm is a downward deflection

    def test_plot_dual(self):
        # Make sure F/F0 looks correct
        signal_vm_ff0 = calc_ff0(self.signal_vm)
        signal_ca_ff0 = calc_ff0(self.signal_ca)

        # Build a figure to plot F/F0 results
        fig_ff0, ax_ff0 = plot_test()
        ax_ff0.set_ylabel('Arbitrary Fluorescent Units')
        ax_ff0.yaxis.set_major_formatter(pltticker.FormatStrFormatter('%.2f'))
        ax_ff0.set_xlabel('Time (ms)')

        ax_ff0.plot(self.time_vm, signal_vm_ff0, color=color_vm, linestyle='None', marker='+', label='Vm, F/F0')
        ax_ff0.plot(self.time_ca, signal_ca_ff0, color=color_ca, linestyle='None', marker='+', label='Ca, F/F0')

        ax_ff0.legend(loc='lower right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        fig_ff0.savefig(dir_tests + '/results/processing_FF0.png')
        fig_ff0.show()


class TestSnrSignal(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.signal_F0 = 1000
        self.signal_amp = 100
        self.signal_t0 = 20
        self.signal_time = 500
        self.noise = 5  # as a % of the signal amplitude
        self.noise_count = 100
        self.time_ca, self.signal_ca = model_transients(model_type='Ca', t0=self.signal_t0, t=self.signal_time,
                                                        f_0=self.signal_F0, f_amp=self.signal_amp, noise=self.noise)

    def test_params(self):
        # Make sure type errors are raised when necessary
        signal_bad_type = np.full(100, True)
        # signal_in : ndarray, dtyoe : uint16 or float
        self.assertRaises(TypeError, calculate_snr, signal_in=True)
        self.assertRaises(TypeError, calculate_snr, signal_in=signal_bad_type)
        # noise_count : int, default is 10
        self.assertRaises(TypeError, calculate_snr, signal_in=self.signal_ca, noise_count=True)
        self.assertRaises(TypeError, calculate_snr, signal_in=self.signal_ca, noise_count='500')

        # Make sure parameters are valid, and valid errors are raised when necessary
        # i_noise : < t, > 0
        self.assertRaises(ValueError, calculate_snr, signal_in=self.signal_ca, noise_count=self.signal_time - 1)
        self.assertRaises(ValueError, calculate_snr, signal_in=self.signal_ca, noise_count=-4)

        # Make sure difficult data is identified
        signal_hard_value = np.full(100, 10, dtype=np.uint16)
        # Peak section too flat for auto-detection
        # signal_hard_value[20] = signal_hard_value[20] + 20.2
        self.assertRaises(ArithmeticError, calculate_snr, signal_in=signal_hard_value)

    def test_results(self):
        # Make sure SNR results are correct
        snr, rms_bounds, peak_peak, sd_noise, ir_noise, ir_peak \
            = calculate_snr(self.signal_ca, noise_count=self.noise_count)
        self.assertIsInstance(snr, float)  # snr
        self.assertIsInstance(rms_bounds, tuple)  # signal_range
        self.assertIsInstance(peak_peak, float)  # Peak to Peak value aka amplitude
        self.assertAlmostEqual(peak_peak, self.signal_amp, delta=self.noise * 4)

        self.assertIsInstance(sd_noise, float)  # sd of noise
        self.assertAlmostEqual(sd_noise, self.noise, delta=1)  # noise, as a % of the signal amplitude
        self.assertIsInstance(ir_noise, np.ndarray)  # indicies of noise
        self.assertIsInstance(ir_peak, np.int32)  # index of peak

        # Make sure a normalized signal (0.0 - 1.0) is handled properly
        signal_norm = normalize_signal(self.signal_ca)
        snr_norm, rms_bounds, peak_peak, sd_noise_norm, ir_noise, ir_peak = \
            calculate_snr(signal_norm, noise_count=self.noise_count)
        self.assertAlmostEqual(snr_norm, snr, delta=1)  # snr
        self.assertAlmostEqual(sd_noise_norm * self.signal_amp, sd_noise, delta=1)  # noise ratio, as a % of

    def test_plot_single(self):
        # Make sure auto-detection of noise and peak regions looks correct
        snr, rms_bounds, peak_peak, sd_noise, ir_noise, ir_peak \
            = calculate_snr(self.signal_ca, noise_count=self.noise_count)

        # Build a figure to plot SNR results
        fig_snr, ax_snr = plot_test()
        ax_snr.set_title('SNR Calculation')
        ax_snr.set_ylabel('Arbitrary Fluorescent Units')
        ax_snr.set_xlabel('Time (ms)')
        ax_snr.set_ylim([self.signal_F0 - 20, self.signal_F0 + self.signal_amp + 20])

        ax_snr.plot(self.time_ca, self.signal_ca, color=gray_light, linestyle='None', marker='+', label='Ca pixel data')

        ax_snr.plot(ir_noise, self.signal_ca[ir_noise], "x", color='r', markersize=2, label='Noise')
        ax_snr.plot_real_noise = ax_snr.axhline(y=self.signal_F0,
                                                color=gray_light, linestyle='--', label='Noise (actual)')
        ax_snr.plot_rms_noise = ax_snr.axhline(y=rms_bounds[0],
                                               color=gray_med, linestyle='-.', label='Noise RMS')

        ax_snr.plot(ir_peak, self.signal_ca[ir_peak], "x", color='g', markersize=10, label='Peaks')
        ax_snr.plot_real_peak = ax_snr.axhline(y=self.signal_F0 + self.signal_amp,
                                               color=gray_light, linestyle='--', label='Peak (actual)')
        ax_snr.plot_rms_peak = ax_snr.axhline(y=rms_bounds[1],
                                              color=gray_med, linestyle='-.', label='Peak RMS')

        ax_snr.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        ax_snr.text(0.65, 0.5, 'SNR (Noise SD, Actual) : {}'.format(self.noise),
                    color=gray_med, fontsize=fontsize2, transform=ax_snr.transAxes)
        ax_snr.text(0.65, 0.45, 'SNR (Noise SD, Calculated) : {}'.format(round(sd_noise, 3)),
                    color=gray_med, fontsize=fontsize2, transform=ax_snr.transAxes)
        ax_snr.text(0.65, 0.4, 'SNR : {}'.format(round(snr, 5)),
                    color=gray_heavy, fontsize=fontsize2, transform=ax_snr.transAxes)
        # ax_snr.text(-1, .18, r'Omega: $\Omega$', {'color': 'b', 'fontsize': 20})

        fig_snr.savefig(dir_tests + '/results/processing_SNRDetection.png')
        fig_snr.show()

    def test_stats(self):
        # Calculate stats (means and variances) of results
        # Trials
        # print('test_stats : sd_noise')
        # print('     Mean : {}'.format(trials1_sd_noise_mean))
        # print('     SD   : {}'.format(trials1_sd_noise_sd))
        trials = [5, 10, 25, 30, 50, 100, 150, 200]
        results = []
        for trial_count in trials:
            result = run_trials_snr(self, trial_count, self.noise)
            results.append(result)

        # Build a figure to plot stats comparison
        labels = [str(i) + ' Trials' for i in trials]
        fig_stats_bar, ax_sd_noise_bar = plot_stats_bars(labels)
        ax_sd_noise_bar.set_title('SNR Accuracy')
        ax_sd_noise_bar.set_ylabel('Noise SD (Calculated)')
        ax_sd_noise_bar.set_xlabel('Calculation Trials')
        ax_sd_noise_bar.set_ylim([3, 7])
        width = 1 / (len(results) + 1)
        for i in range(0, len(results)):
            x_tick = (1 / len(results)) * i
            ax_sd_noise_bar.bar(x_tick, results[i]['sd_noise']['mean'], width, color=gray_med, fill=True,
                                yerr=results[i]['sd_noise']['sd'], error_kw=dict(lw=1, capsize=4, capthick=1.0))
        ax_sd_noise_bar.real_sd_noise = ax_sd_noise_bar.axhline(y=self.noise, color=gray_light, linestyle='--',
                                                                label='Noise SD (Actual)')
        ax_sd_noise_bar.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        # fig_stats_bar.show()

        # Scatter plot with error bars
        fig_stats_scatter, ax_sd_noise_scatter = plot_stats_scatter()
        ax_sd_noise_scatter.set_title('SNR Accuracy')
        ax_sd_noise_scatter.set_ylabel('Noise SD (Calculated)')
        ax_sd_noise_scatter.set_xlabel('Calculation Trials')
        ax_sd_noise_scatter.set_ylim([3, 7])
        for i in range(0, len(results)):
            ax_sd_noise_scatter.errorbar(trials[i], results[i]['sd_noise']['mean'],
                                         yerr=results[i]['sd_noise']['sd'], fmt="x",
                                         color=gray_heavy, lw=1, capsize=4, capthick=1.0)

        ax_sd_noise_scatter.real_sd_noise = ax_sd_noise_scatter.axhline(y=self.noise, color=gray_light,
                                                                        linestyle='--', label='Noise SD (Actual)')
        ax_sd_noise_scatter.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_stats_scatter.show()

    def test_error(self):
        # Error values at different noise values
        noises = range(2, 10)
        trial_count = 20
        results_trials_snr = []
        for noise in noises:
            result = run_trials_snr(self, trial_count, noise)
            results_trials_snr.append(result)

        error, error_mean, error_sd = calculate_error(np.asarray(noises),
                                                      np.asarray([result['sd_noise']['mean']
                                                                  for result in results_trials_snr]))

        # Build a figure to plot stats comparison
        fig_error_scatter, ax_snr_error_scatter = plot_stats_scatter()
        ax_snr_error_scatter.set_title('SNR vs Noise Accuracy (n={})'.format(trial_count))
        ax_snr_error_scatter.set_ylabel('SNR (Noise SD, Calculated)', color=gray_med)
        # ax_snr_error_scatter.set_ylabel('%Error of SNR Calculation')
        ax_snr_error_scatter.set_xlabel('SNR (Noise SD, , Actual)')
        ax_snr_error_scatter.set_ylim([0, noises[-1] + 1])
        ax_snr_error_scatter.set_xlim([0, noises[-1] + 1])
        ax_snr_error_scatter.tick_params(axis='y', labelcolor=gray_med)
        ax_snr_error_scatter.grid(True)
        for i in range(0, len(noises)):
            ax_snr_error_scatter.errorbar(noises[i], results_trials_snr[i]['sd_noise']['mean'],
                                          yerr=results_trials_snr[i]['sd_noise']['sd'], fmt="x",
                                          color=gray_med, lw=1, capsize=4, capthick=1.0)

        ax_error = ax_snr_error_scatter.twinx()  # instantiate a second axes that shares the same x-axis
        ax_error.baseline = ax_error.axhline(color=gray_light, linestyle='-.')
        ax_error.set_ylabel('%Error of SNR')  # we already handled the x-label with ax1
        ax_error.set_ylim([-100, 100])
        ax_error.plot(noises, error, color=gray_heavy, linestyle='-', label='% Error')

        ax_error.legend(loc='lower right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_error_scatter.show()


class TestSnrMap(unittest.TestCase):
    def setUp(self):
        # Setup data to test with, a propagating stack of varying SNR
        self.f_0 = 1000
        self.f_amp = 100
        self.noise = 3
        self.d_noise = 10  # as a % of the signal amplitude
        self.noise_count = 100
        self.time_ca, self.stack_ca = model_stack_propagation(
            model_type='Ca', d_noise=self.d_noise, f_0=self.f_0, f_amp=self.f_amp, noise=self.noise)
        self.FRAMES = self.stack_ca.shape[0]
        self.HEIGHT, self.WIDTH = (self.stack_ca.shape[1], self.stack_ca.shape[2])
        self.frame_shape = (self.HEIGHT, self.WIDTH)
        self.origin_x, self.origin_y = self.WIDTH / 2, self.HEIGHT / 2
        self.div_borders = np.linspace(start=int(self.HEIGHT / 2), stop=self.HEIGHT / 2 / 5, num=5)

    def test_params(self):
        # Make sure type errors are raised when necessary
        # stack_in : ndarray, 3-D array
        stack_bad_shape = np.full((100, 100), 100, dtype=np.uint16)
        stack_bad_type = np.full(self.stack_ca.shape, True)
        self.assertRaises(TypeError, map_snr, stack_in=True)
        self.assertRaises(TypeError, map_snr, stack_in=stack_bad_shape)
        self.assertRaises(TypeError, map_snr, stack_in=stack_bad_type)
        # noise_count : int
        self.assertRaises(TypeError, map_snr, stack_in=self.stack_ca, noise_count=True)

        # Make sure parameters are valid, and valid errors are raised when necessary
        # noise_count : >=0
        self.assertRaises(ValueError, map_snr, stack_in=self.stack_ca, noise_count=-2)

    def test_results(self):
        # Make sure SNR Map results are correct
        snr_map_ca = map_snr(self.stack_ca)
        self.assertIsInstance(snr_map_ca, np.ndarray)  # snr map type
        self.assertEqual(snr_map_ca.shape, self.frame_shape)  # snr map shape
        self.assertIsInstance(snr_map_ca[0, 0], float)  # snr map value type

    def test_plot(self):
        # Make sure SNR Map looks correct
        snr_map_ca = map_snr(self.stack_ca)
        snr_max = np.nanmax(snr_map_ca)
        snr_min = np.nanmin(snr_map_ca)
        print('SNR Maps max value: ', snr_max)

        # Plot a frame from the stack and the SNR map of that frame
        fig_map_snr, ax_img_snr, ax_map_snr = plot_map()
        ax_img_snr.set_title('Noisy Model Data (noise SD: {}-{})'.format(self.noise, self.noise + self.d_noise))
        ax_map_snr.set_title('SNR Map')
        # Frame from stack
        cmap_frame = SCMaps.grayC.reversed()
        img_frame = ax_img_snr.imshow(self.stack_ca[0, :, :], cmap=cmap_frame)
        # Draw circles showing borders of SNR variance
        for idx, div_border in enumerate(self.div_borders):
            div_circle = Circle((self.origin_x, self.origin_y), radius=div_border,
                                fc=None, fill=None, ec=gray_light, lw=1, linestyle='--')
            ax_img_snr.add_artist(div_circle)
        ax_img_snr.set_ylabel('1.0 cm', fontsize=fontsize3)
        ax_img_snr.set_xlabel('0.5 cm', fontsize=fontsize3)
        ax_map_snr.set_ylabel('1.0 cm', fontsize=fontsize3)
        ax_map_snr.set_xlabel('0.5 cm', fontsize=fontsize3)
        # Add colorbar (lower right of frame)
        ax_ins_img = inset_axes(ax_img_snr, width="5%", height="80%", loc=5,
                                bbox_to_anchor=(0.15, 0, 1, 1), bbox_transform=ax_img_snr.transAxes,
                                borderpad=0)
        cb_img = plt.colorbar(img_frame, cax=ax_ins_img, orientation="vertical")
        cb_img.ax.set_xlabel('Intensity\n(a.u).', fontsize=fontsize3)
        cb_img.ax.yaxis.set_major_locator(pltticker.LinearLocator(2))
        cb_img.ax.yaxis.set_minor_locator(pltticker.LinearLocator(10))
        cb_img.ax.tick_params(labelsize=fontsize3)
        # SNR Map
        # Create normalization range for map (0 and max rounded up to the nearest 10)
        cmap_snr = SCMaps.tokyo
        cmap_norm = colors.Normalize(vmin=0, vmax=round(snr_max + 5.1, -1))
        img_snr = ax_map_snr.imshow(snr_map_ca, norm=cmap_norm, cmap=cmap_snr)
        # Add colorbar (lower right of map)
        ax_ins_map = inset_axes(ax_map_snr, width="5%", height="80%", loc=5,
                                bbox_to_anchor=(0.15, 0, 1, 1), bbox_transform=ax_map_snr.transAxes,
                                borderpad=0)
        cb1_map = plt.colorbar(img_snr, cax=ax_ins_map, orientation="vertical")
        cb1_map.ax.set_xlabel('SNR', fontsize=fontsize3)
        cb1_map.ax.yaxis.set_major_locator(pltticker.LinearLocator(5))
        cb1_map.ax.yaxis.set_minor_locator(pltticker.LinearLocator(10))
        cb1_map.ax.tick_params(labelsize=fontsize3)

        fig_map_snr.show()
        fig_map_snr.savefig(dir_tests + '/results/processing_SNRMap_ca.png')


class TestErrorSignal(unittest.TestCase):
    def setUp(self):
        # Setup data to test with
        self.signal_F0 = 1000
        self.signal_amp = 100
        self.signal_t0 = 20
        self.signal_time = 500
        self.noise = 10  # as a % of the signal amplitude
        self.noise_count = 100
        self.time_ca_ideal, self.signal_ca_ideal = model_transients(model_type='Ca', t0=self.signal_t0,
                                                                    t=self.signal_time,
                                                                    f_0=self.signal_F0, f_amp=self.signal_amp)
        self.time_ca_mod, self.signal_ca_mod = model_transients(model_type='Ca', t0=self.signal_t0, t=self.signal_time,
                                                                f_0=self.signal_F0, f_amp=self.signal_amp,
                                                                noise=self.noise)

    def test_params(self):
        # Make sure type errors are raised when necessary
        signal_bad_type = np.full(100, True)
        # ideal : ndarray, dtyoe : uint16 or float
        # modified : ndarray, dtyoe : uint16 or float
        self.assertRaises(TypeError, calculate_error, ideal=True, modified=self.signal_ca_mod)
        self.assertRaises(TypeError, calculate_error, ideal=signal_bad_type, modified=self.signal_ca_mod)
        self.assertRaises(TypeError, calculate_error, ideal=self.signal_ca_ideal, modified=True)
        self.assertRaises(TypeError, calculate_error, ideal=self.signal_ca_ideal, modified=signal_bad_type)

    def test_results(self):
        # Make sure Error results are correct
        error, error_mean, error_sd = calculate_error(self.signal_ca_ideal, self.signal_ca_mod)
        self.assertIsInstance(error, np.ndarray)  # error
        self.assertIsInstance(error_mean, float)  # error_mean
        self.assertIsInstance(error_sd, float)  # error_sd

        self.assertAlmostEqual(error.max(), self.noise / 3, delta=1)
        self.assertAlmostEqual(error_mean, 0, delta=0.1)
        self.assertAlmostEqual(error_sd, self.noise / 10, delta=1)  # error_sd

    def test_plot(self):
        # Make sure error calculation looks correct
        error, error_mean, error_sd = calculate_error(self.signal_ca_ideal, self.signal_ca_mod)
        # Build a figure to plot SNR results
        fig_snr, ax_error_signal = plot_test()
        ax_error_signal.set_title('%Error of a noisy signal')
        ax_error_signal.set_ylabel('Arbitrary Fluorescent Units', color=gray_med)
        ax_error_signal.tick_params(axis='y', labelcolor=gray_med)
        ax_error_signal.set_xlabel('Time (ms)')

        ax_error_signal.plot(self.time_ca_ideal, self.signal_ca_ideal, color=gray_light, linestyle='-',
                             label='Ca, ideal')
        ax_error_signal.plot(self.time_ca_mod, self.signal_ca_mod, color=gray_med, linestyle='None', marker='+',
                             label='Ca, {}% noise'.format(self.noise))

        ax_error = ax_error_signal.twinx()  # instantiate a second axes that shares the same x-axis
        ax_error.set_ylabel('%')  # we already handled the x-label with ax1
        ax_error.set_ylim([-10, 10])
        # error_mapped = np.interp(error, [-100, 100],
        #                          [self.signal_ca_mod.min(), self.signal_ca_mod.max()])
        ax_error.plot(self.time_ca_ideal, error, color=gray_heavy, linestyle='-',
                      label='% Error')
        # ax_error.tick_params(axis='y', labelcolor=gray_heavy)

        ax_error_signal.legend(loc='upper left', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        ax_error.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)
        fig_snr.show()

    def test_stats(self):
        # Calculate stats (means and variances) of results
        # Error values at different noise values
        noises = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        results = []
        for noise in noises:
            result = {'error': {'array': np.empty(10), 'mean': 0, 'sd': 0}}
            time_ca_mod, signal_ca_mod = model_transients(model_type='Ca', t0=self.signal_t0, t=self.signal_time,
                                                          f_0=self.signal_F0, f_amp=self.signal_amp,
                                                          noise=noise)
            error, error_mean, error_sd = calculate_error(self.signal_ca_ideal, signal_ca_mod)
            result['error']['array'] = error
            result['error']['mean'] = error_mean
            result['error']['sd'] = error_sd
            results.append(result)

        # Build a figure to plot stats comparison
        fig_stats_scatter, ax_sd_noise_scatter = plot_stats_scatter()
        ax_sd_noise_scatter.set_title('%Error of Noisy vs Ideal data')
        ax_sd_noise_scatter.set_ylabel('%Error (Mean w/ SD)')
        ax_sd_noise_scatter.set_xlabel('Noise SD (Actual)')
        ax_sd_noise_scatter.set_ylim([-10, 10])
        for i in range(0, len(results)):
            ax_sd_noise_scatter.errorbar(noises[i], results[i]['error']['mean'],
                                         yerr=results[i]['error']['sd'], fmt="x",
                                         color=gray_heavy, lw=1, capsize=4, capthick=1.0)

        ax_sd_noise_scatter.real_sd_noise = ax_sd_noise_scatter.axhline(y=0, color=gray_light, linestyle='--')
        # ax_sd_noise_scatter.legend(loc='upper right', ncol=1, prop={'size': fontsize2}, numpoints=1, frameon=True)

        fig_stats_scatter.show()


if __name__ == '__main__':
    unittest.main()
