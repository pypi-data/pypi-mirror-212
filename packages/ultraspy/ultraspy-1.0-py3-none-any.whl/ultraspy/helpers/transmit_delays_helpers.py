"""Helpers needed for computing transmitted delays if not provided.
"""
import numpy as np


def convert_3d_angles_to_focus(angle_lateral, angle_elevational, focus=10):
    """Converting the lateral and elevational angles to positive focuses for
    plane wave imaging.

    :param float angle_lateral: The lateral tilting of the plane wave
    :param float angle_elevational: The elevational tilting of the plane wave
    :param float focus: The focus point (in m). It is set to 10m by default,
        to simulate plane focus, thus plane waves.

    :returns: Blabla
    :return type: numpy.ndarray

    %- Outputs -----------------------------------------------------------%
    %   - focus (matrix) : matrix of focus of size (Nangles x 3) with a
    %       norm of 10 [m] with x, y, and z along columns.
    %
    %- Dependencies ------------------------------------------------------%
    %   - 'sph2cart' function
    %
    %- Example -----------------------------------------------------------%
    %    TX_angles = deg2rad([[-7.5, 0]; [-3.75, 0]; [0, -7.5]; [0, -3.75]; [0, 0]; [0, 3.75]; [0, 7.5]; [3.75, 0]; [7.5, 0]]);
    %    TX_focus = angles2focus(TX_angles);
    """
    return None


def compute_pw_delays(angles, probe, speed_of_sound=1540.,
                      transmission_mode='positives'):
    """Computes the transmission delays to send the plane waves with the given
    angles based on the probes used and the transmission mode.

    :param numpy.ndarray angles: The list of the angles to send, in radians
    :param Probe probe: The probe class with the information relative to the
        elements geometry and coordinates
    :param float speed_of_sound: The estimated speed of sound of the medium to
        compute the transmission delays (default is 1540)
    :param str transmission_mode: The mode of transmission depending on the
        used convention. Can either be 'positives', setting all the delays to
        positive values, 'negatives', the opposite, or 'centered', where the
        maximum delay is equal to minus the minimum delay (only used in Picmus
        to my knowledge)

    :returns: The delays for all the angles and probes elements, of shape
        (nb_angles, nb_probe_elements)
    :return type: numpy.ndarray
    """
    if transmission_mode not in ['positives', 'centered', 'negatives']:
        raise AttributeError(
           "Transmission mode needs to be either 'positives', 'centered' or "
           "'negatives'.")

    assert all(abs(angles.ravel()) < np.pi / 2), \
           "Angles must be in radians (|angle| < pi / 2)"

    # If any angles in the elevational axis are given, compute 2D delays (got
    # a matricial probe)
    if angles.ndim == 2 and angles[1, :].any():
        assert probe.geometry_type == 'matricial', \
            "3D delays will be computed, the probe must be matricial."
        # return compute_3d_pw_delays()
        raise NotImplementedError("3D delays")

    # Work only on lateral axis for angles
    if angles.ndim == 2:
        angles = angles[0, :]

    # Plane wave along the lateral axis
    x_coords = probe.geometry[0, :]
    distances = x_coords[None, :] * np.sin(angles[:, None])
    # If convex, needs to add the axial distances of the probes elements
    if probe.geometry_type == 'convex':
        z_coords = probe.geometry[2, :]
        distances += z_coords[None, :]

    # Convert to delays
    delays = distances / speed_of_sound

    # Make all of them positives
    delays -= np.min(delays)

    # Distinct transmission modes
    if transmission_mode == 'centered':
        delays -= (np.max(delays) / 2)
    elif transmission_mode == 'negatives':
        delays -= np.max(delays)

    return delays
