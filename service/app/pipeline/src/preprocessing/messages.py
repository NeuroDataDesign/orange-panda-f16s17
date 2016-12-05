import pandas as pd
def clean(format):
  message = """
        <h3>CLEANING DATA</h3>
        <ul>
          <li>
            Extracted EEG data with %(n_chans)s channels
            and %(n_obs)s observations.
          </li> 
          <li>
            Extracted timing data with %(n_obs)s timesteps sampled
            at %(freq_times)s observations per %(freq_unit)s.
          </li>
          <li>
            Extraced coordinate data of the %(n_chans)s channels
            in measured in %(coord_unit)s coordinates.
          </li>
        </ul>
        """ % format
  return message

def zeroed_electrodes(format):
  message = """
    <h3> DETECTING ZEROED CHANNELS </h3>
    <ul>
      <li>
        Discovered %(n_zeroed_chans)s zeroed channels.
      </li>
      <li>
        Zeroed channels were %(zeroed_chans)s.
      </li>
      <li>
        Removed the zeroed channels? (%(rm_zero)s)
      </li>
    </ul>
    """ % format
  return message

def bad_detec(format):
  message = """
    <h3> DETECTING BAD CHANNELS </h3>
    <h5> Detecting bad channels with the %(bad_detec_method)s method. </h5>
    <ul>
      <li>
        Discovered %(n_bad_chans)s bad channels.
      </li>
      <li>
        Bad channels were %(bad_chans)s.
      </li>
    </ul>
    <h5> Plot of the bad channels: </h5>
    """ % format
  return message

def interp(format):
  message = """
    <h3> INTERPOLATING BAD CHANNELS </h3>
    <h5> Interpolating with %(interp_method)s method. </h5>
    <ul>
      <li>
        Interpolated the electrodes %(bad_chans)s.
      </li>
      <li>
        Interpolated against nearest %(interp_npts)s electrodes.
      </li>
    </ul>
    <h5> Plot of the interpolated channels: </h5>
    """ % format
  return message

def red_noise(format):
  message = """
    <h3>REDUCING NOISE</h3>
    <ul>
    <li>Highpass filtered at .1 Hz threshold.</li>
    <li>Bandstop filtered at harmonics of 60Hz.</li>
    </ul>
    """ % format
  return message

def eye_artifact(format):
  message = """
    <h3> DETECTING AND REMOVING ARTIFACTS </h3>
    <h5> Discovering artifacts with %(eye_artifact_method)s. </h5>
    <ul>
      Discovered independent components.
    </ul>
    """ % format
  return message