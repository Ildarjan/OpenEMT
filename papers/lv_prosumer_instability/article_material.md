# Connection-Triggered Control Oscillations in a Low-Voltage Prosumer Feeder: A Reproducible EMT Case Study

## Draft abstract

The connection of distributed inverters changes the dynamic electrical environment of a low-voltage feeder, even when its passive line and transformer impedances remain unchanged. This study investigates a connection-triggered oscillatory response in a 400 V radial network supplying twenty single-phase households, ten of which are equipped with inverter generation. Nine inverters initially operate with moderate power-control gains. At 3 s, a remotely located inverter with deliberately aggressive integral gains is connected and its active-power reference is ramped to 3.5 kW. Electromagnetic transient simulations using an averaged voltage-source model show a growing voltage envelope on the connected phase. Controlled comparisons separate the influence of integral gains, feeder impedance, and the connection event, while integration-step refinement checks the numerical persistence of the response. A multivariable feedback formulation explains how voltage sensitivity, active/reactive power coupling, and delayed power measurements can reduce damping. The study provides a reproducible counterexample to the assumption that individually specified power references guarantee a stable interconnected operating condition. Its conclusions concern the implemented outer power controller; a general penetration threshold, a measured impedance stability margin, and a detailed commercial inverter response are not established.

Keywords: low-voltage distribution; prosumers; distributed generation; inverter interaction; impedance-based stability; electromagnetic transients; power control.

## Main scientific summary

Increasing prosumer participation introduces controlled sources at electrically distributed points. Their incremental current response to terminal voltage is frequency dependent. Connecting another source changes both the operating point and the aggregate closed-loop admittance seen by existing units. It does not, by itself, increase the physical resistance or inductance of the feeder. Consequently, counting inverters or reporting installed capacity alone cannot identify the stability boundary.

In this experiment, the distinguishing perturbation is the connection of one aggressively tuned unit. Nine units already operate at the same dispatch with moderate gains. The experiment therefore supports a claim about controller compatibility in a particular network. It does not show that a tenth normally tuned inverter is intrinsically unstable, or that 50% prosumer penetration is a universal limit.

The proposed physical explanation is a feedback interaction: a current change modifies the local voltage through network impedance; voltage and angle changes modify measured active and reactive power; the controller corrects the internal voltage magnitude and frequency using delayed measurements; the resulting current can reinforce the initial deviation. Low-voltage resistance makes active/reactive coupling relevant. Excessive integral gain can reduce damping in this coupled loop. The observed waveform growth supports this interpretation, but an eigenvalue or measured-admittance calculation is still needed to prove the precise unstable mode.

## Mathematical formulation

### 1. Network and converter equations

For inverter k, define current positive from the internal source toward its AC terminal. The averaged filter branch is

\[
L_{f,k}\dot i_k=e_k-v_k-R_{f,k}i_k,\qquad
e_k=\sqrt{2}E_k\sin(\theta_k+\phi_k).
\]

The phase assignment is represented by phi_k. The actual code uses global phase indices for single-phase laterals. The neutral is an ideal reference in this case; a finite neutral conductor and neutral displacement are absent.

The implemented dispatch controller is described using p and q in kW and kvar, respectively:

\[
\dot\theta_k=2\pi\left[f_0+m_p(p_k^*-p_{f,k})+\xi_{P,k}\right],
\quad \dot\xi_{P,k}=k_{iP}(p_k^*-p_{f,k}),
\]
\[
E_k=E_0+m_q(q_k^*-q_{f,k})+\xi_{Q,k},
\quad \dot\xi_{Q,k}=k_{iQ}(q_k^*-q_{f,k}).
\]

The frequency trim xi_P is in Hz and the voltage trim xi_Q is in V. Integral gains have units Hz/(kW s) and V/(kvar s). This block is called GFL dispatch in the software, but its internal oscillator and controlled EMF do not constitute a conventional PLL plus inner current-loop implementation.

For a single-phase inverter, voltage and current are projected onto its own rotating reference and averaged over one nominal cycle, T0 = 20 ms. For example,

\[
V_r=\sqrt{2}\langle v\sin\theta\rangle_{T_0},\quad
V_i=\sqrt{2}\langle v\cos\theta\rangle_{T_0},
\]
\[
p_m=(V_rI_r+V_iI_i)/1000,\quad
q_m=(V_iI_r-V_rI_i)/1000,
\]
\[
T_f\dot p_f=p_m-p_f,\qquad T_f\dot q_f=q_m-q_f.
\]

A baseband approximation to the measurement transfer function is

\[
H(s)\approx\frac{1-e^{-sT_0}}{sT_0}\frac{1}{1+sT_f}.
\]

This expression is a continuous approximation to the discrete projection buffers and first-order update in the code. It is not an exact harmonic transfer model of an unbalanced single-phase system.

### 2. Why resistance couples the power loops

Consider an explanatory two-source equivalent, with E exp(j delta) behind Z = R + jX and a reference voltage V. Receiving-terminal injected power S = V I* gives

\[
P=\frac{V}{R^2+X^2}\{R(E\cos\delta-V)+XE\sin\delta\},
\]
\[
Q=\frac{V}{R^2+X^2}\{X(E\cos\delta-V)-RE\sin\delta\}.
\]

Near E = V and delta = 0, the local sensitivity is

\[
\begin{bmatrix}\Delta P\\\Delta Q\end{bmatrix}
\approx\frac{1}{R^2+X^2}
\begin{bmatrix}V^2X&VR\\-V^2R&VX\end{bmatrix}
\begin{bmatrix}\Delta\delta\\\Delta E\end{bmatrix}.
\]

Here P and Q are in W and var. Divide this Jacobian by 1000 when combining it with the controller gains above. For appreciable R/X, the off-diagonal terms cannot be discarded. This two-source equivalent illustrates the coupling; the feeder requires a nodal Jacobian evaluated at its actual loaded operating point, including filter dynamics and all connected converters.

### 3. Closed-loop stability condition

Let J(s) map all converter angle and magnitude perturbations to power perturbations after elimination of passive network variables. For fixed references, define

\[
C(s)=\operatorname{blockdiag}_k\left\{
\begin{bmatrix}
\frac{2\pi}{s}(m_p+k_{iP}/s)&0\\
0&m_q+k_{iQ}/s
\end{bmatrix}\right\}.
\]

With measurement matrix H(s), the feedback characteristic equation is

\[
\det[I+C(s)H(s)J(s)]=0.
\]

An oscillatory instability corresponds to a conjugate pole pair with positive real part. A fitted growing voltage envelope can suggest this condition; it does not replace computing the poles. Increasing gains changes loop magnitude, while measurement averaging and integration add phase lag. Network impedance changes J(s), so a controller setting cannot be judged independently of the network.

An alternative nodal impedance formulation uses converter current positive INTO the converter, so Delta i_c = Y_c(s) Delta v. With passive network admittance Y_n(s),

\[
\det[Y_n(s)+Y_c(s)]=0,
\quad\text{or}\quad
\det[I+Z_n(s)Y_c(s)]=0.
\]

The second form requires an invertible grounded network admittance. Connecting converter k changes the relevant assembled admittance by its port contribution. For a multi-node feeder this is a matrix insertion, not a scalar sum at one PCC. Generalized Nyquist analysis must include the open-loop unstable pole count [1,2]. No Nyquist curve is claimed to have been calculated in the present package.

## Case specification and reproducibility

The source case is `examples/lv_04kv_rooftop_pv.json`. Exact inputs for every run are saved beside the CSV data. The network contains a 10/0.4 kV transformer, five 100 m feeder sections, twenty household laterals, and ten inverter locations assigned A/B/C = 4/3/3. The transformer is represented by Dy11 with a grounded secondary star. Its primary delta branch leakage is R = 14.4 ohm and L = 145.8 mH, corresponding to approximately 4% leakage impedance on the stated 250 kVA base. The nominal rating is a study assumption, not a thermal constraint in the block.

Each feeder section has R = 0.096 ohm and L = 0.153 mH. At 50 Hz the five sections sum to 0.48 + j0.2403 ohm, with R/X approximately 2.0. These are deliberately selected weak-feeder study impedances. A specific commercial cable construction is not validated. Loads are passive parallel R-L branches; their exact values are retained in the circuit snapshots. The DC energy source is idealized and the single-phase AC current limiter is disabled. Large post-instability voltages and currents must therefore be interpreted as model responses, not device survival predictions.

All inverters have a 3.5 kW active-power reference and zero reactive-power reference. Nine use kiP = 0.2, kiQ = 2, Lf = 3 mH and Tf = 20 ms. Inverter 719 uses kiP = 0.6, kiQ = 40, Lf = 1 mH and Tf = 40 ms. Common proportional gains are mp = 0.05 Hz/kW and mq = 0.4 V/kvar; filter resistance is 0.15 ohm. The remote unit connects at 3 s with a 150 ms reference ramp. Its disconnected oscillator free-runs at 50 Hz; the model does not implement a synchronism-check relay or a PLL. Connection mismatch is a possible excitation of the unstable response and should be separated from modal stability in follow-up work.

The integration duration is 5 s. Runs use 100, 50 and 25 microsecond steps and a common 250 microsecond output interval. Data columns are time, phase RMS voltages at bus 105, inverter 719 active/reactive power and RMS current. The API uses one-cycle windowed quantities. The first 0.5 s is omitted from plotted views to focus on the operating interval; raw startup samples remain in the CSV files. Display-window endpoint conventions can change small residual RMS ripples, so large-envelope comparisons and step refinement are preferred over millivolt claims.

The comparison named `retuned_50us` changes only the remote inverter integral gains to 0.2 and 2. Its filter and measurement time constant remain unchanged. The comparison `stiff_50us` divides feeder R and L by three while preserving transformer leakage and inverter tuning. `nine_only_50us` moves connection beyond the simulation window. These controlled interventions must be read from the exported results rather than assumed to stabilize the system.

## Proposed article structure and writing plan

1. **Introduction (600 to 800 words).** Explain distributed generation, dynamic interactions and the distinction between hosting capacity and dynamic stability. State the narrow research question: can a remotely connected controller excite an otherwise quiet LV feeder?
2. **Network and converter model (900 to 1200 words).** Present the topology, parameter table, branch equations, power estimator and controller. Explain neutral and device-limit assumptions before interpreting results.
3. **Stability framework (800 to 1100 words).** Derive the local R/X power sensitivity and matrix feedback condition. Separate explanatory theory from quantities actually identified from the numerical model.
4. **Experimental design (500 to 700 words).** Specify connection/ramp timing, measurement windows, unchanged parameters in each comparison and integration-step refinement. Include code and circuit hashes in final supplementary material.
5. **Results (800 to 1000 words).** Present connection response, controlled comparisons and numerical refinement in that order. Quote computed metrics from `data/metrics.json`; discuss residual variation rather than rounding it into apparent exact convergence.
6. **Discussion (600 to 900 words).** Explain phase localization, controller dependence and the role of network sensitivity. Discuss why fixed physical impedance can coexist with a changed dynamic equivalent. Avoid extrapolating a general penetration threshold.
7. **Conclusions (200 to 300 words).** State only findings supported by comparisons. Identify the finite-neutral and detailed-converter extensions needed for deployment-oriented conclusions.

Before submission, extend the study with a loaded-operating-point linearization or measured multiport admittance, a controller-gain/impedance stability boundary, small synchronized perturbations after settling, explicit neutral impedance, and validated protection/current-limit behavior. These are proposed work, not completed results. A longer simulation is also needed before calling a finite-window oscillation asymptotically unstable or a comparison asymptotically stable.

## Figure captions

**Figure 1.** Connection-triggered response at the remote feeder bus and inverter 719. The vertical line denotes connection at 3 s; shading denotes the 150 ms dispatch ramp. Voltages are phase-to-reference RMS values. P and Q use the API generator sign convention. Traces begin at 0.5 s; raw data include startup.

**Figure 2.** Controlled comparisons at a 50 microsecond integration step. Only integral gains change in the retuned case; only feeder R and L change in the reduced-impedance case; the nine-inverter comparison has no connection during the run. The lower panel exposes the current excursions that accompany voltage oscillation.

**Figure 3.** Integration-step refinement for the aggressive-controller case. The 100, 50 and 25 microsecond runs share a 250 microsecond output interval. Persistence of the oscillatory response under refinement supports numerical robustness of the qualitative result; waveform differences remain relevant to quantitative claims.

## References and scope of attribution

[1] Bo Wen, **Inverse Nyquist Stability Criterion for Grid-Tied Inverters**, Virginia Tech CPES research summary, 2018. https://cpes.vt.edu/library/view_nugget/768/ . Supports the impedance-ratio formulation and pole-accounting caveat.

[2] Yicheng Liao and Xiongfei Wang, **Impedance-Based Stability Analysis for Interconnected Converter Systems with Open-Loop RHP Poles**, author manuscript, arXiv:1811.09237, revised 2019. https://arxiv.org/abs/1811.09237 . Supports the need to account for open-loop right-half-plane poles in interconnected converter analysis.

[3] **Frequency Coupling Suppression Control Strategy for Single-Phase Grid-Tied Inverters in Weak Grid**, research record, Eindhoven University of Technology. https://research.tue.nl/en/publications/frequency-coupling-suppression-control-strategy-for-single-phase-/ . Establishes frequency coupling as a relevant issue in detailed single-phase converter models. Its PLL-related mechanism is not attributed to the present PLL-free model.

All figures in this package are original simulations of the supplied OpenEMT case. The equations describing its dispatch law were transcribed from `src/blocks.js`; the two-source sensitivity and feedback formulation are analytical interpretation, not a claimed published validation of this specific implementation.
