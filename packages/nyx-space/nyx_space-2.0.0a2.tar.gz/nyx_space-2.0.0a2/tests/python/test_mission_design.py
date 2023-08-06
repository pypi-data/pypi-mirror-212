import logging
from pathlib import Path
import pickle

from nyx_space.cosmic import Spacecraft, Orbit, SrpConfig, Cosm
from nyx_space.mission_design import (
    propagate,
    StateParameter,
    Event,
    SpacecraftDynamics,
    TrajectoryLoader,
)
from nyx_space.time import Duration, Unit, Epoch, TimeSeries


def test_propagate():
    # Initialize logging
    FORMAT = "%(levelname)s %(name)s %(filename)s:%(lineno)d\t%(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    # Base path
    root = Path(__file__).joinpath("../../../").resolve()

    config_path = root.joinpath("./data/tests/config/")

    sc = Spacecraft.load(str(config_path.joinpath("spacecraft.yaml")))
    # Check that we have loaded this correctly by checking the values from the YAML file
    assert sc.value_of(StateParameter.X) == -9042.862234
    assert sc.value_of(StateParameter.Y) == 18536.333069
    assert sc.value_of(StateParameter.Z) == 6999.957069
    assert sc.value_of(StateParameter.VX) == -3.288789
    assert sc.value_of(StateParameter.VY) == -2.226285
    assert sc.value_of(StateParameter.VZ) == 1.646738
    assert sc.value_of(StateParameter.Cr) == 1.0
    assert sc.value_of(StateParameter.Cd) == 2.2
    assert sc.value_of(StateParameter.FuelMass) == 50.0
    assert sc.epoch.timedelta(Epoch("2018-09-15T00:15:53.098 UTC")) == Duration.zero()
    # Check other stuff that is computed on request
    assert sc.value_of(StateParameter.SMA) == 21999.99774705774

    dynamics = SpacecraftDynamics.load_named(str(config_path.joinpath("dynamics.yaml")))
    # So far, there are no accessors on the dynamics, so we will check what they print out =(
    assert (
        f"{dynamics['lofi']}"
        == "Spacecraft dynamics (with guidance = false): No force models; Orbital dynamics: Point masses of Sun J2000, Earth J2000"
    )
    assert (
        f"{dynamics['hifi']}"
        == "Spacecraft dynamics (with guidance = false): SRP with φ = 1367 W/m^2 and eclipse light-source: Sun J2000, shadows casted by: Sun J2000, Moon J2000;  Orbital dynamics: Point masses of Sun J2000, Earth J2000, Moon J2000; IAU Earth gravity field 10x10 (order x degree)"
    )

    rslt, traj = propagate(sc, dynamics["lofi"], Unit.Day * 5.159)
    # Check that we propagated for the correct duration
    assert rslt.epoch.timedelta(sc.epoch) == Duration("5 days 3 h 48 min 57 s 600 ms")
    # We aren't in two body dynamics so the SMA has changed among other things.
    assert rslt.value_of(StateParameter.SMA) == 22000.024381883788
    # Grab a specific epoch from the trajectory
    sc_state = traj.at(Epoch("2018-09-16T00:16:53 TDB"))
    # Check that we got the right epoch
    assert sc_state.epoch.timedelta(Epoch("2018-09-16T00:16:53 TDB")) == Duration.zero()
    # Save the file to parquet
    traj.to_parquet("lofi.parquet")

    # We can also propagate with a different method
    rslt, traj = propagate(sc, dynamics["lofi"], Unit.Day * 5.159, method="Dormand78")
    assert rslt.epoch.timedelta(sc.epoch) == Duration("5 days 3 h 48 min 57 s 600 ms")

    # Let's now propagate the original spacecraft to its apoapsis, but let's search no more than 2 orbit periods
    rslt_apo, _ = propagate(
        sc,
        dynamics["lofi"],
        sc.orbit.period() * 2,
        event=Event(StateParameter.Apoapsis, 0.0),
    )
    # Let's make sure that worked to within the default precision
    assert abs(rslt_apo.value_of(StateParameter.TrueAnomaly) - 180.0) < 0.001

    event = Event(StateParameter.Apoapsis, 0.0, value_precision=1e-6)

    # But we can also be even more precise
    rslt_apo, traj = propagate(
        sc,
        dynamics["lofi"],
        sc.orbit.period() * 2,
        event=event,
    )
    assert abs(rslt_apo.orbit.ta_deg() - 180.0) <= 1e-6

    # Resample the trajectory at fixed step size of 25 seconds
    traj = traj.resample(Unit.Second * 25.0)

    # Export this trajectory with additional metadata and the events
    traj.to_parquet(
        "lofi_with_events.parquet", metadata={"test key": "test value"}, events=[event]
    )

    # Also export this ground track
    cosm = Cosm.de438()
    iau_earth = cosm.frame("IAU Earth")
    traj.to_parquet("iau_earth_lofi.parquet", groundtrack=iau_earth)

    # Let's also search for this event in the trajectory
    for sc_at_event in traj.find(event):
        print(sc_at_event)
        assert abs(sc_at_event.value_of(StateParameter.TrueAnomaly) - 180.0) <= 1e-6


def test_build_spacecraft():
    """
    Tests that we can build a spacecraft from scratch without an input file
    """
    # Initialize logging
    FORMAT = "%(levelname)s %(name)s %(filename)s:%(lineno)d\t%(message)s"
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.INFO)

    cosm = Cosm.de438()
    eme2k = cosm.frame("EME2000")  # Earth Mean Equator J2000
    orbit = Orbit.from_keplerian_altitude(
        400.0, 0.01, 15.6, 45.0, 90.0, 75.0, Epoch.system_now(), eme2k
    )
    # Define the SRP
    srp = SrpConfig(2.0)  # 2.0 will be the area
    print(srp)
    assert srp.cr == 1.8  # Default value
    assert srp.area_m2 == 2.0
    sc = Spacecraft(orbit, 150.0, 15.0, srp)
    print(sc)

    assert sc.srp().__eq__(srp)  # Not sure why the `==` operator doesn't work here
    assert sc.drag().area_m2 == 0.0
    assert (
        sc.drag().cd == 2.2
    )  # Default value, but the area is zero, so it doesn't have any effect

    # Using this spacecraft as a template, let's load an OEM file, convert it to Parquet, and ensure we can load it back in.
    # The orbit data will be overwritten with data from the OEM file.
    root = Path(__file__).joinpath("../../../").resolve()

    config_path = root.joinpath("./data/tests/ccsds/oem/LEO_10s.oem")
    output_path = root.joinpath("./output_data/LEO_10s.parquet")
    # Convert from OEM to Parquet will happen on load
    traj = TrajectoryLoader(str(config_path), "oem", str(output_path), sc)
    print(traj)
    # Check that we can pickle the trajectory loader object
    traj_pkl = pickle.dumps(traj)
    traj_unpkl = pickle.loads(traj_pkl)
    assert traj_unpkl.__eq__(traj)
    # Check that we can convert this to a spacecraft trajectory
    traj_sc = traj.to_spacecraft_traj()
    traj_orbit = traj.to_orbit_traj()
    traj_orbit_dc = traj_sc.downcast()
    # Check that we can query it (will raise an exception if we can't, thereby failing the test)
    ts = TimeSeries(Epoch("2020-06-01T12:00:00.000000"), Epoch("2020-06-01T13:00:00.000000"), step=Unit.Minute*17 + Unit.Second*13.8, inclusive=True)
    for epoch in ts:
        orbit = traj_orbit.at(epoch)
        dc_orbit = traj_orbit_dc.at(epoch)
        sc_orbit = traj_sc.at(epoch).orbit
        # Check params individually
        assert orbit.epoch == sc_orbit.epoch
        assert orbit.x_km == sc_orbit.x_km
        assert orbit.vx_km_s == sc_orbit.vx_km_s
        # Check the downcasted version
        assert dc_orbit.x_km == sc_orbit.x_km
        assert dc_orbit.vx_km_s == sc_orbit.vx_km_s
        assert dc_orbit.__eq__(sc_orbit)



if __name__ == "__main__":
    # test_propagate()
    test_build_spacecraft()
