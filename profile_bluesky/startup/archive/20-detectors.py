print(__file__)

"""various detectors and other signals"""

aps = APS_devices.ApsMachineParametersDevice(name="APS")
#sd.baseline.append(aps)

aps_current = aps.current
#sd.monitors.append(aps_current)

# NOTE: These are some possible check_beam-style actions:
#if aps.inUserOperations:
#    # no scans until A_shutter is open
#    # suspend_A_shutter = bluesky.suspenders.SuspendFloor(A_shutter.pss_state, 1)
#    # #suspend_A_shutter.install(RE)
#    # RE.install_suspender(suspend_A_shutter)
#
#    # no scans if aps.current is too low
#    # don't restart automatically since more things need to be adjusted
#    # so, set restart current threshold to 10 A, APS will never get to that current, scan won't restart
#    suspend_APS_current = bluesky.suspenders.SuspendFloor(aps_current, 2, resume_thresh=10000)
#    RE.install_suspender(suspend_APS_current)


scaler = ScalerCH('3idb:scaler1', name='scaler')
scaler.match_names()
APS_devices.use_EPICS_scaler_channels(scaler)


# userCalcs_3idc = APS_devices.userCalcsDevice("3idc:", name="userCalcs_3idc")


energy_scan = SscanRecord("3idb:scan1", name="energy_scan")
#energy_scan.stage_sigs["positioners.p1.setpoint_pv"] = test_energy.user_setpoint.pvname
#energy_scan.stage_sigs["positioners.p1.readback_pv"] = test_energy.user_readback.pvname
#energy_scan.stage_sigs["positioners.p1.start"] = -0.1
#energy_scan.stage_sigs["positioners.p1.end"] = 0.1
#energy_scan.stage_sigs["positioners.p1.step_size"] = 0.1
#for d in range(1, 9):
#    energy_scan.stage_sigs[f"detectors.d0{d}.input_pv"] = scaler.prefix + f".S{d}"
#energy_scan.stage_sigs["refd"] = 6  # reference detector (scaler channel number)
#energy_scan.stage_sigs["triggers.d1.trigger_pv"] = scaler.prefix + ".CNT"
#energy_scan.stage_sigs["triggers.d1.trigger_value"] = 1
#energy_scan.stage_sigs["pasm"] = "PEAK POS" # 3


from ophyd.mca import EpicsMCA
mca = EpicsMCA("3ida:mca1", name="mca")
