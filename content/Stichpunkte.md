# Thesis Writing Guide — Stichpunkte

> ±10 bullet points per chapter/section/subsection.
> Depth and style modeled after Huhnstock's dissertation (2022).
> Specific equations to derive are named explicitly.
> Chapters 7–9 (Protein transport, Tissue, WLI) are deferred.

---

## Chapter 1: Introduction

1. Open with the broad vision: Lab-on-a-chip (LOC) devices for diagnostics/analytics; magnetic particles as mobile carriers for analyte capture, transport, and detection
2. Narrow to magnetophoresis — using non-uniform magnetic fields to move particles near surfaces; cite key reviews (Pamme, Gijs, Ehresmann group)
3. Introduce the IBMP-based transport concept: exchange-bias thin film substrates + external oscillating fields → traveling wave MFL that drives particles laterally (cite Holzinger, Ehresmann group works)
4. State the key advance over Huhnstock: separation by *surface chemistry* (COOH vs NH₂) rather than by size or pattern geometry — enabled by DLVO-mediated height differences
5. Mention the prototypical stripe domain pattern (5 µm width, hh/tt) as the established workhorse; reference Huhnstock's focus/separation patterns as context
6. Highlight the critical frequency ν_c as the central observable linking drag, magnetic force, and particle–substrate distance
7. State the role of the polymer spacer layer (P(MMA-co-AA), 700 nm) in tuning electrostatic interactions without changing the MFL
8. Summarize what the paper (Small, 2026) demonstrated: statistically significant separation of ν_c for COOH (6.47 Hz) vs NH₂ (4.29 Hz) particles under identical magnetic conditions
9. Outline the thesis structure chapter-by-chapter (1–2 sentences each)
10. Optionally mention DFG funding context (CRC/TRR 270, SPP 1681, etc.)

**Figure**: Schematic of the transport concept (substrate cross-section with MFL + particle + external fields)

---

## Chapter 2: Theoretical Background

### 2.1 Magnetism

#### 2.1.1 Atomic magnetism

1. Orbital angular momentum **L** and associated magnetic moment **μ_L** = −μ_B **L**/ℏ; define Bohr magneton μ_B = eℏ/2m_e
2. Spin angular momentum **S** and spin magnetic moment **μ_S** = −g_s μ_B **S**/ℏ with g_s ≈ 2
3. Total angular momentum **J** = **L** + **S** via Russel-Saunders (LS) coupling; derive **μ_J** and Landé g-factor g_J
4. Hund's rules for determining ground-state L, S, J
5. Quenching of orbital angular momentum in 3d transition metals (crystal field argument) — relevant because Co₇₀Fe₃₀ is the FM layer
6. Diamagnetism, paramagnetism: Curie law χ = C/T
7. Connect to this work: the FM layer (Co₇₀Fe₃₀) and the AF layer (Ir₁₇Mn₈₃) are both 3d-based, so orbital quenching and exchange dominate

**Equations**: μ_B = eℏ/2m_e; **μ_J** = −g_J μ_B **J**/ℏ; Landé g_J formula; Curie law

#### 2.1.2 Magnetic interactions

1. **Exchange interaction**: origin from Pauli exclusion + Coulomb repulsion → Heisenberg Hamiltonian Ĥ = −Σ J_ij **S_i** · **S_j**
2. Direct exchange vs. indirect exchange (RKKY, superexchange) — mention RKKY as relevant for AF coupling across spacers
3. Bethe-Slater curve: sign of J vs. interatomic distance ratio r_a/r_3d → explain why Fe, Co, Ni are ferromagnetic
4. **Dipolar interaction**: derive energy E_dip = (μ₀/4πr³)[**μ₁**·**μ₂** − 3(**μ₁**·**r̂**)(**μ₂**·**r̂**)] — weak compared to exchange but important for long-range particle–particle interactions and stray fields
5. **Spin-orbit coupling**: H_SO = ξ **L**·**S** → couples spin system to lattice, origin of magnetocrystalline anisotropy
6. Discuss ordering: ferromagnetic, antiferromagnetic, ferrimagnetic; Curie temperature T_C, Néel temperature T_N
7. Mean-field / Weiss molecular field approach for T_C
8. Connect to this work: exchange defines FM ordering in CoFe; AF ordering in IrMn sets T_N ≈ 520 K (above field-cooling temperature 300 °C = 573 K); dipolar interaction governs stray fields from domain pattern

**Equations**: Heisenberg Hamiltonian; dipolar energy; H_SO; Weiss molecular field

**Figure**: Bethe-Slater curve

#### 2.1.3 Thin film magnetism

1. Magnetic domains: Weiss domains minimize magnetostatic energy; domain walls (Bloch vs. Néel) — define widths and energies
2. Domain wall energy: competition of exchange stiffness A and anisotropy K → wall width δ_DW ~ π√(A/K)
3. Single-domain vs. multi-domain: critical size argument
4. Hysteresis loop: define M_s, M_r, H_c; sketch idealized loop
5. In thin films: Néel walls preferred (film thickness < wall width); reduced dimensionality → enhanced surface/interface effects
6. Thin film growth modes (Volmer-Weber, Frank–van der Merwe, Stranski-Krastanov) — brief, since sputtered polycrystalline films
7. Polycrystalline microstructure: grain boundaries, texture effects on anisotropy and exchange coupling
8. Magnetic charge model for stray field calculation: volume charges ρ_V = −∇·**M**, surface charges σ_S = **M**·**n̂** → derive **H_stray** from these
9. Apply magnetic charge model to hh/tt stripe pattern: show that head-to-head and tail-to-tail DWs produce maximum stray field gradients; side-by-side DWs weaker
10. Connect to this work: the Cu/IrMn/CoFe/Si layer stack is polycrystalline RF-sputtered; 5 µm stripe width chosen for reliable hh/tt IBMP patterning; stray field drives particle transport

**Equations**: δ_DW; ρ_V, σ_S; stray field integrals for stripe pattern

**Figure**: Schematic of Bloch vs. Néel wall; magnetic charges at hh/tt domain walls

#### 2.1.4 Magnetic particles

1. Superparamagnetism: below critical size, thermal fluctuations overcome anisotropy barrier → no remanence; define blocking temperature T_B
2. Néel relaxation time τ_N = τ₀ exp(KV/k_BT) — thermal switching of single-domain nanoparticles
3. Brownian relaxation time τ_B = 3ηV_H / k_BT — physical rotation of entire particle in viscous medium
4. Effective relaxation: 1/τ_eff = 1/τ_N + 1/τ_B — for the micromer-M particles (2 µm, magnetite inclusions), Brownian dominates
5. Magnetization response: Langevin function L(α) = coth(α) − 1/α where α = μ₀mH/k_BT
6. Effective susceptibility χ_eff for low fields: linear regime M ≈ χ_eff H; measured values χ_COOH = 0.26, χ_NH₂ = 0.27
7. Particle structure: polystyrene matrix with embedded magnetite (Fe₃O₄) nanoparticles, 2.2–4.0 wt% magnetic content
8. Discuss polydispersity (d = 2.0 ± 0.4 µm) and its effect on critical frequency distribution
9. Literature context: different SPB types (Dynabeads, micromer-M, chemicell) — compare Huhnstock's M-270 Carboxylic Acid (d = 2.8 µm) with this work's micromer-M (d = 2.0 µm)
10. Connect to this work: identical magnetic content (χ) but different surface chemistry → separation must arise from DLVO-mediated height differences, not magnetic force differences

**Equations**: τ_N; τ_B; Langevin function; low-field susceptibility approximation

**Figure**: Sketch of SPB structure (polystyrene matrix + magnetite nanoparticles); Langevin function plot

---

### 2.2 Magnetic anisotropy

#### 2.2.1 Magnetocrystalline anisotropy

1. Origin: spin-orbit coupling links spin orientation to crystal lattice → energy depends on magnetization direction
2. Uniaxial anisotropy (hcp Co): E_ani = K₁ sin²θ + K₂ sin⁴θ; define easy/hard axis
3. Cubic anisotropy (bcc Fe, fcc Ni): E_ani = K₁(α₁²α₂² + …)
4. CoFe alloys: depend on composition; Co₇₀Fe₃₀ — primarily uniaxial due to hcp-like local order in polycrystalline films
5. Temperature dependence of K; at high T → K → 0
6. Anisotropy field H_K = 2K/(μ₀M_s) — field needed to saturate along hard axis
7. Role in exchange bias: the FM anisotropy determines H_c of the FM layer
8. Connect to this work: CoFe magnetocrystalline anisotropy is moderate; the dominant anisotropy contribution is exchange bias (unidirectional)

**Equations**: Uniaxial E_ani; cubic E_ani; H_K

#### 2.2.2 Shape anisotropy

1. Demagnetizing field **H_d** = −**N**·**M** with demagnetization tensor **N** (trace = 1)
2. Shape anisotropy energy: E_shape = (μ₀/2)(N_⊥ − N_∥)M_s² sin²θ
3. Thin film limit: N_⊥ ≈ 1 → strong in-plane preference, which is the case for the 10 nm CoFe layer
4. For stripe domains: effective demagnetization depends on stripe width-to-thickness ratio
5. In SPBs: sphere N = 1/3 → no net shape anisotropy → isotropic response (consistent with Langevin behavior)
6. Connect to this work: the thin-film shape anisotropy keeps CoFe magnetization in-plane; this is essential for the hh/tt domain configuration

**Equations**: **H_d**; E_shape for thin film

#### 2.2.3 Surface and interface anisotropies

1. Néel model: broken symmetry at surfaces/interfaces → additional anisotropy K_eff = K_V + 2K_S/t (two interfaces)
2. Perpendicular magnetic anisotropy (PMA) in ultrathin films: K_S can overcome shape anisotropy → out-of-plane magnetization
3. For CoFe(10 nm): film is thick enough that in-plane magnetization is maintained (shape dominates)
4. Interface anisotropy at IrMn/CoFe and CoFe/Si interfaces: contributes to effective EB field and coercivity
5. Roughness and intermixing at interfaces → reduces K_S
6. Connect to this work: interface quality is controlled by RF sputtering parameters; field-cooling procedure (300 °C, 60 min) may cause some interdiffusion

**Equations**: K_eff = K_V + 2K_S/t

---

### 2.3 Exchange bias

1. Phenomenology: FM/AF bilayer after field-cooling below T_N → hysteresis loop shifted by H_EB; also increased H_c (training effect)
2. Discovery: Meiklejohn & Bean (1956), Co/CoO core-shell nanoparticles
3. **Meiklejohn-Bean model**: single-crystal, uncompensated AF interface; derive H_EB = −J_int / (μ₀ M_FM t_FM) from energy balance of Zeeman + exchange + anisotropy
4. Derive condition for EB: K_AF t_AF > J_int (AF must be "rigid"); discuss AF spin-flop condition
5. Limitations of Meiklejohn-Bean: predicts H_EB orders of magnitude too large for polycrystalline systems
6. **Polycrystalline model** (Fulcomer & Charap / two-energy-level): AF consists of grains with distribution of sizes and anisotropy axes; each grain has two stable states with energy barrier ΔE = K_AF V_AF
7. Thermal activation: grains with ΔE < 25 k_BT are thermally unstable → do not contribute to EB; grains with ΔE ≫ k_BT are "frozen" → contribute
8. Field-cooling procedure: 300 °C → above T_N of IrMn; cool in 150 mT → sets unidirectional anisotropy direction for all AF grains
9. IrMn composition: Ir₁₇Mn₈₃ → T_N ≈ 520 K; chosen for high T_N and suitable grain size distribution
10. **He ion bombardment modification**: keV He⁺ ions cause atomic displacements in AF layer → reorient AF grain moments if external field applied during bombardment
11. Dose dependence: competing creation and destruction of EB; derive competing exponential model: H_EB(D) = H_EB,0 [a·exp(−D/D₁) − (1−a)·exp(−D/D₂)]
12. Optimal dose for reversal: D ≈ 1–2.5 × 10¹⁵ ions/cm² at 10 keV → this work uses 2.5 × 10¹⁵/cm²
13. Resist-masked IBMP: photolithography defines 5 µm stripes; He⁺ passes through open areas → bombarded regions reverse H_EB direction → hh/tt domain configuration
14. Discuss resulting domain pattern magnetically: double hysteresis in VSM/MOKE; MFM confirms hh/tt and ss domain walls
15. Connect to this work: the 5 µm hh/tt pattern with H_EB,IB ≈ −H_EB,0 produces maximum stray field gradients for particle transport

**Equations**: Meiklejohn-Bean H_EB; AF rigidity condition; competing exponential dose model; field-cooling protocol rationale

**Figures**: Schematic of field-cooling; hysteresis loop shift; IBMP process flow (resist → bombardment → strip); double hysteresis (VSM)

---

### 2.4 DLVO-Forces

#### 2.4.1 Electrostatic interactions

1. Origin: charged surfaces in aqueous solution → electrical double layer (Helmholtz/Stern + diffuse layer)
2. Zeta potential: measured at slipping plane; proxy for surface potential; depends on pH, ionic strength, surface functionalization
3. Debye-Hückel approximation: linearized Poisson-Boltzmann → exponential decay; Debye length κ⁻¹ = √(εε₀k_BT / (2N_Ae²I))
4. For sphere-plate geometry (SPB above flat substrate): derive electrostatic force F_el(z) using constant-potential or constant-charge boundary conditions
5. Constant-potential vs. constant-charge: discuss which applies (likely constant-charge for oxide/polymer surfaces during fast transport)
6. pH dependence of ζ: acidic → protonation → ζ ↑ (positive); basic → deprotonation → ζ ↓ (negative); isoelectric point
7. For this work: ζ_COOH = −45 mV, ζ_NH₂ = −35 mV, ζ_substrate = −45 mV (all pH 7, ddH₂O) → different surface charge densities → different repulsion from substrate
8. Debye length in ddH₂O: κ⁻¹ ≈ 960 nm (very large, since I ≈ 10⁻⁷ M) → electrostatic interaction extends far
9. Connect to this work: the 10 mV difference in ζ between COOH and NH₂ causes different equilibrium heights → different drag → different ν_c

**Equations**: Debye length κ⁻¹; electrostatic force for sphere-plate; relation between ζ and σ

**Figure**: Sketch of electrical double layer (Stern + diffuse); ζ vs. pH curves for COOH/NH₂

#### 2.4.2 Van der Waals

1. Origin: London dispersion forces between fluctuating dipoles → always attractive for identical/similar materials across a medium
2. Hamaker approach: integrate pair-wise Lennard-Jones over two macroscopic bodies; Hamaker constant A_H
3. Sphere-plate vdW force: F_vdW(z) = −A_H R / (6z²) (non-retarded, Derjaguin approximation)
4. Retardation correction: at large separations (z > λ/2π ≈ 20 nm), electromagnetic retardation weakens attraction → Gregory correction factor f(z) = 1/(1 + 14z/λ)
5. Hamaker constant for polystyrene/water/Si system: estimate A_H ≈ 1.0–1.3 × 10⁻²⁰ J from combining relation
6. At equilibrium distances of 100–300 nm (as expected from ζ differences), vdW is weak but non-negligible — primarily determines the "sticking" threshold at very small distances
7. Discuss: P(MMA-co-AA) spacer modifies the effective A_H at the top surface compared to bare Si capping
8. Connect to this work: vdW is the same for COOH and NH₂ (same polystyrene matrix, same Hamaker constant) → separation arises purely from electrostatic difference

**Equations**: F_vdW (non-retarded); Gregory retardation factor; Hamaker combining relation

---

### 2.5 Traveling wave magnetophoresis

#### 2.5.1 Particle transport mechanism

1. **Actuation concept**: superposition of static MFL (from EB domain pattern) with time-varying homogeneous external fields → dynamically transformed potential energy landscape
2. Literature review of alternative actuation methods: permanent magnets, micro-coils, soft/hard magnetic surface elements, domain-wall-based transport in garnet films; cite key references per method
3. Compare: IBMP-based approach advantages — topographically flat, lithographically defined, tunable by ion dose, switchable patterns
4. **Magnetic force on SPB**: F_mag = μ₀Vχ_eff/(μ₀(1+χ_eff/3)) · (H_eff · ∇)H_eff (for linear susceptibility regime)
5. Potential energy landscape: U(x,z) ∝ −|H_eff(x,z)|²; minima above domain walls where |H_z| is largest
6. **Transport cycle**: describe the 4-step trapezoidal field sequence (Hx+, Hz+, Hx−, Hz−) with π/2 phase shift → particle follows shifting potential minimum by one stripe period d per cycle
7. Derive critical frequency: ν_c = F_mag,max / (f_D(z) · d) where f_D(z) is the z-dependent friction coefficient → maximum frequency at which particle completes each step
8. Velocity-frequency relation: v(ν) = ν·d for ν ≤ ν_c (phase-locked); v(ν) = (ν − √(ν² − ν_c²))·d for ν > ν_c (phase-slipping)
9. Critical frequency defined as 50% of linear-regime velocity ("half-max" criterion from paper)
10. Trapezoidal pulse shape: define rise time Δt_r, plateau time Δt_p, drop time Δt_d; alteration rate 4000 mT/s; values: Δt_r,x = 1144 µs, Δt_r,z = 1294 µs
11. One-dimensional transport: only x and z pulse sequences with π/2 phase shift; two-dimensional if y-pulse added (not used in this work)
12. Connect to this work: the v(ν) model is fitted to mean ensemble velocities for COOH and NH₂ separately → single free parameter ν_c extracted per particle type

**Equations**: magnetic force (gradient form); potential energy; ν_c definition; v(ν) relations; trapezoidal timing

**Figure**: Schematic of 4-step transport cycle with field directions and particle positions; v(ν) plot showing phase-locked/phase-slipping

#### 2.5.2 Close to surface transport

1. **Equilibrium height**: force balance F_mag,z(z) + F_vdW(z) + F_el(z) = 0 determines particle–substrate distance z_eq
2. Goldman correction for near-wall hydrodynamic drag: f_D(z) = 6πηR · f(z/R) with f(z/R) a series expansion (Brenner/Goldman, 5 terms used in paper); drag increases dramatically as particle approaches surface (f → ∞ for z → 0)
3. Magnetophoretic mobility: μ_mag = v_ss / F_mag = 1/f_D(z_eq) → directly linked to equilibrium height
4. Key insight: particle floating higher → lower drag → higher ν_c; floating lower → higher drag → lower ν_c
5. Why COOH has higher ν_c: ζ_COOH = −45 mV vs. ζ_NH₂ = −35 mV → COOH is repelled more from substrate (ζ_s = −45 mV) → floats higher → less drag → higher ν_c = 6.47 Hz vs. 4.29 Hz
6. Theoretical estimate: calculate z_eq for both particle types using measured ζ values, Debye length, Hamaker constant, MFL from simulation → predict height difference of ~10–30 nm → corresponds to significant drag difference via Goldman correction
7. Stray field simulation: OOMMF micromagnetic simulation of the hh/tt stripe magnetization pattern → extract H_z(x,z) and H_x(x,z) at various elevations → compute F_mag(z) above DW center
8. Steady-state velocity: v_ss = F_mag,x(z_eq) / f_D(z_eq); depends exponentially on z_eq because both F_mag and f_D vary strongly with height
9. Sensitivity analysis: show that ν_c is very sensitive to z_eq; a 20 nm height difference produces a ~30–50% change in ν_c
10. Discuss: in Huhnstock Ch. 5, similar COOH/NH₂ comparison but with 800 nm Si capping → found marginal differences in mobility; this work uses 700 nm polymer spacer and achieves clear separation (ν_c,COOH/ν_c,NH₂ = 1.51)
11. Role of spacer material: P(MMA-co-AA) with ζ = −45 mV vs. Huhnstock's Si/SiO₂ with ζ ≈ −35 mV → polymer enhances the electrostatic differentiation
12. Connect to this work: this section provides the theoretical framework for interpreting v(ν) curves and extracting ν_c as a quantitative separation metric

**Equations**: force balance for z_eq; Goldman drag series; μ_mag; v_ss

**Figure**: Force vs. distance plot showing intersection (equilibrium height); schematic of height-dependent drag mechanism

---

## Chapter 3: Experimental Methods

### 3.1 Particle transport setup

1. 3D Helmholtz coil setup: three orthogonal coil pairs from copper wire; describe radius, number of windings, calibration factors (mT/V) per direction
2. Trapezoidal magnetic field pulses: controlled by NI box + LabVIEW; parameters: H_x,max = 2.3 mT, H_z,max = 2.6 mT, alteration rate 4000 mT/s
3. Optical microscopy: Zeiss Axiotech D reflective microscope; dark-field illumination (required for opaque EB substrates); objectives 20× (0.4 NA) and 50×
4. High-speed camera: EoSense 2.0 MCX12-CM, monochromatic, 1920 × 1080 px, up to ~2000 fps; this work records at 1000 fps for 5 s → 5000 frames
5. Image cropping: 1920 × 1080 → 1408 × 1080 to avoid fringe illumination artifacts
6. Microfluidic chamber: Parafilm spacer (~120 µm thick) with 8 × 8 mm central opening on 15 × 15 mm substrate; sealed with cover slip; 10 µL of 8 × 10⁶ MPs/mL dispersion in ddH₂O
7. MP preparation: micromer-M (micromod, d = 2.0 ± 0.4 µm) stock diluted to 8 × 10⁶/mL; COOH and NH₂ surface functionalizations
8. Setup placed on vibration-damped platform (concrete plate / air cushions)
9. Sample positioning: xy stage for different ROIs
10. Explain principle of dark-field microscopy briefly: only scattered light from particles reaches detector → particles appear bright on dark background

**Figure**: Schematic of setup (coils + microscope + camera); photo of chamber assembly

### 3.2 Transport substrate preparation

1. Base: 15 × 15 mm naturally oxidized Si(100) → cleaned with isopropanol + N₂ drying
2. Layer stack deposition by RF sputtering: Cu(10 nm) / Ir₁₇Mn₈₃(30 nm) / Co₇₀Fe₃₀(10 nm) / Si(10 nm) at room temperature, 35 mT during deposition
3. Field-cooling: anneal at 300 °C for 60 min in 150 mT external field → sets exchange bias direction
4. Lithography: spin-coat photoresist (AR-P 5350, ALLRESIST), UV expose through 5 µm stripe shadow mask, develop → ~600 nm resist mask
5. Ion bombardment: 10 keV He⁺ from home-built Penning source; 2.5 × 10¹⁵/cm²; 80 mT opposing original EB → bombarded stripes reverse H_EB → hh/tt pattern
6. Resist removal: TechniStrip NI555 at 80 °C for 2 h + ultrasonication 3 min + acetone/isopropanol/N₂ rinse
7. Spacer layer: spin-coat P(MMA-co-AA) copolymer (AR-P 617.06, ALLRESIST) → soft-bake 100 °C / 10 min → total t_spacer ≈ 710 nm (including 10 nm Si cap)
8. Spacer purpose: topographic smoothness + electrostatic surface potential (ζ_s = −45 mV) → tunes particle–substrate interaction

**Figure**: Process flow diagram (layer deposition → field-cool → litho → IBMP → strip → spacer coat)

### 3.3 Thin film sputter deposition

1. PVD principle: physical transfer of target material to substrate via momentum transfer in Ar plasma
2. DC sputtering: two-electrode setup; Ar⁺ accelerated to negatively biased cathode (target); sputtered atoms deposit on substrate (anode)
3. Limitations of DC: charge buildup on insulating targets → need RF
4. RF sputtering (used here): 13.56 MHz AC; self-bias mechanism on target; impedance matching; can sputter insulators (Si cap layer)
5. Leybold Heraeus Z400 system: base pressure, Ar flow, sputter rates per target material
6. Deposition under 35 mT → induces uniaxial anisotropy in CoFe during growth
7. Substrate rotation for uniformity (if applicable)
8. Compare typical rates: Cu ≈ 3.6 nm/min, CoFe ≈ 3.0 nm/min, IrMn ≈ 5.5 nm/min, Si ≈ 3.5 nm/min

### 3.4 Ion bombardment induced magnetic patterning

1. Principle: keV He⁺ ions penetrate thin film → nuclear/electronic energy loss → atomic displacements in AF grains → randomize AF spin configuration
2. With external field during bombardment: displaced AF spins re-orient along applied field → reverses EB if field opposes original direction
3. Ion range: 10 keV He⁺ in Cu/IrMn/CoFe/Si → SRIM simulations show ions penetrate through full stack with peak damage in IrMn layer
4. Dose optimization: too low dose → incomplete reversal; too high → structural damage → loss of EB; optimal for this stack: 2.5 × 10¹⁵/cm²
5. Penning source: home-built; describe ion extraction principle briefly, beam homogeneity, current measurement
6. Resist mask: AR-P 5350 photoresist, ~600 nm thick, absorbs He⁺ → protects underlying regions; 5 µm stripe openings define domain width
7. Shadow mask vs. laser-writer lithography: this work uses shadow mask (standard 5 µm stripes); Huhnstock used laser-writer for complex focus/separation patterns
8. Magnetic field during bombardment: 80 mT, antiparallel to original EB → ensures full reversal in open stripes
9. Result: alternating hh/tt domain configuration with maximum magnetic charge contrast at DWs
10. Verification: MOKE/VSM (double hysteresis) + MFM (monopolar phase contrast at stripe boundaries)

**Figure**: IBMP schematic (ions + resist + field); SRIM depth profile; MFM image of resulting pattern

### 3.5 Magnetic characterization

#### 3.5.1 MOKE magnetometry

1. **Principle**: linearly polarized light reflected from magnetized surface acquires Kerr rotation (and ellipticity) proportional to magnetization component
2. Physical origin: spin-orbit coupling modifies dielectric tensor → off-diagonal elements ∝ M → Fresnel coefficients change → polarization state modified
3. Three MOKE geometries: polar, longitudinal, transverse — depending on **M** vs. incidence plane; longitudinal (L-MOKE) used here (in-plane M in plane of incidence)
4. L-MOKE setup: laser source, polarizer, sample, analyzer, photodetector; applied field via electromagnet
5. Sensitivity: surface-sensitive (penetration depth ~20 nm for visible light in metals) → probes FM layer directly
6. Local measurement: laser spot size defines probed area (typically ~100 µm) → can characterize specific regions of patterned sample
7. For this work: L-MOKE measures M(H) hysteresis of EB-patterned substrates → confirms double hysteresis with H_EB,left and H_EB,right
8. Compare VSM (integral) vs. MOKE (local) → discrepancies in H_EB values due to local variations

**Equations**: Kerr rotation angle ∝ off-diagonal dielectric tensor element (conceptual)

#### 3.5.2 Vibrating sample magnetometry

1. **Principle**: sample vibrates sinusoidally in uniform magnetic field → time-varying magnetic flux through nearby pickup coils → induced voltage ∝ M
2. Faraday's law: V_ind = −dΦ/dt ∝ m · ω · cos(ωt) → lock-in detection at vibration frequency extracts M
3. Pickup coil geometry: saddle coils or Helmholtz-type; calibration with known Ni standard
4. M(H) sweep: extract M_s, H_c, H_EB, M_r/M_s (squareness)
5. Integral technique: measures total magnetic moment of entire sample → averages over bombarded + non-bombarded regions
6. For EB-patterned samples: double hysteresis → fit with two arctan functions to extract H_EB and H_c for each sub-loop
7. For MPs: measure M(H) to extract M_sat, χ_eff → used to compute magnetic force; this work: M = 4.8 A·m²/kg, M_sat > 6.5
8. Instrument: specify model used in this work

**Equations**: V_ind ∝ dM/dt; two-arctan fit function for double hysteresis

#### 3.5.3 Magnetic force microscopy

1. **Principle**: scanning probe method; AFM cantilever with magnetic (CoCr) coating → two-pass technique: 1st pass topography (tapping), 2nd pass magnetic signal at lift height
2. Signal: frequency/phase shift of cantilever oscillation in lift pass due to magnetic tip–sample interaction
3. Derive: interaction energy E_int = −μ₀ ∫ **M_s** · **H_t** dV → for thin film with surface/volume charges: E_int = ∫ σ_S Φ_t dS + ∫ ρ_V Φ_t dV
4. MFM signal: phase shift Δφ ∝ ∂²E_int/∂z² → sensitive to second derivative of stray field
5. Weak-interaction assumption: tip does not perturb sample magnetization → verify by measuring with opposite tip magnetizations (contrast should invert)
6. Resolution: depends on tip radius, lift height, coating thickness; typical ~50 nm lateral
7. For this work: confirm hh/tt domain configuration via monopolar phase contrast at DW positions; measure stripe width, domain wall quality
8. MFM cannot determine absolute magnetization direction → need micromagnetic simulations for corroboration
9. Instrument: Nanosurf FlexAFM with C3000 controller or specify actual instrument
10. Connect: MFM images validate the magnetic pattern before transport experiments

**Equations**: E_int with magnetic charges; phase shift relation

**Figure**: Example MFM phase image of hh/tt stripe pattern with line profile

#### 3.5.4 Magnetophoretic velocity measurement away from any wall

1. Purpose: measure χ_eff of individual MP types by tracking particle velocity in known field gradient far from surfaces (bulk, unconfined)
2. Method: apply inhomogeneous field (e.g., from permanent magnet or single coil) → track particle velocity → extract F_mag from Stokes drag → compute χ
3. Stokes drag: F_D = 6πηRv (no Goldman correction far from walls) → χ_eff = F_D / (μ₀V_p/(1+χ/3) · H∇H)
4. Results: χ_COOH = 0.26 ± 0.01, χ_NH₂ = 0.27 ± 0.01 → effectively identical within uncertainty
5. Significance: rules out magnetic force differences as cause of ν_c separation → points to DLVO-mediated height difference
6. Instrument/method details: describe specific setup or reference to standard magnetophoretic mobility measurement

#### 3.5.5 Dynamic light scattering: Zeta potential

1. **Principle**: electrophoretic light scattering — particles in electric field → electrophoretic mobility μ_E measured via Doppler shift of scattered laser light
2. Henry equation: μ_E = 2εε₀ζ f(κa) / (3η) → convert μ_E to ζ
3. Smoluchowski limit: f(κa) → 1.5 for large particles (κa ≫ 1) — check: κ⁻¹ ≈ 960 nm, a = 1 µm → κa ≈ 1 → Hückel/Henry correction needed
4. Instrument: Zetasizer Nano ZS90 (Malvern); measurement at pH 7 in ddH₂O
5. Results: ζ_COOH = −45 mV, ζ_NH₂ = −35 mV → 10 mV difference drives separation mechanism
6. pH dependence: COOH → carboxylate deprotonation above pH ~4 → strongly negative; NH₂ → amine protonation below pH ~9 → less negative at neutral pH
7. Substrate ζ: measured or estimated from literature for P(MMA-co-AA) surface → ζ_s ≈ −45 mV
8. Significance: these three ζ values are the primary inputs for the DLVO equilibrium height calculation

**Equations**: Henry equation; κa parameter

---

## Chapter 4: Particle Transport Evaluation Software

> Already well-written; only minor additions needed.

1. Keep current trackpy/Crocker-Grier exposition as-is
2. Add brief paragraph: choice of dark-field vs. bright-field for particle detection (dark-field: particles bright on dark background → `invert=False` in trackpy; different from Huhnstock who used bright-field)
3. Add: comparison to Huhnstock's Video Spot Tracker / AdaPT → trackpy advantage: automated batch processing, no manual selection, reproducible
4. Ensure filtering criteria are justified quantitatively (current table is good)
5. Mention: IQR outlier removal for ν_c extraction (from paper)

---

## Chapter 5: Surface-Surface Interaction Based Separation

### 5.1 Characterization of Superparamagnetic Particles

#### 5.1.1 Zeta potential

1. Present ζ measurements: COOH = −45 mV, NH₂ = −35 mV at pH 7 in ddH₂O; include error bars and number of measurements
2. Show pH-dependence curves if measured (or refer to manufacturer data); compare with Huhnstock Fig. 5.1 for same particle types
3. Substrate ζ: P(MMA-co-AA) surface measured → −45 mV; compare with literature values for SiO₂ (Huhnstock used ≈ −35 mV)
4. Discuss the chemistry: COOH groups → carboxylate (COO⁻) at pH 7 → strongly negative; NH₂ → partially protonated (NH₃⁺) at pH 7 → less negative
5. Compute predicted surface charge densities σ from ζ via Grahame equation
6. Compute Debye length for ddH₂O (κ⁻¹ ≈ 960 nm) → very long-range electrostatic interaction
7. Compare: COOH–substrate repulsion (same ζ = −45 mV) is stronger than NH₂–substrate repulsion (−35 mV vs −45 mV)
8. Setup: Zetasizer measurement conditions, sample preparation (dilution, temperature, equilibration)

**Table**: ζ values for COOH, NH₂, substrate; χ values; particle properties

#### 5.1.2 Magnetophoretic velocity

1. Present χ measurements: COOH = 0.26 ± 0.01, NH₂ = 0.27 ± 0.01 → identical within uncertainty
2. Method: as described in Ch. 3.5.4
3. Compute resulting magnetic force difference: < 4% → negligible compared to electrostatic effect
4. M(H) curves from VSM: show Langevin-like response for both; extract M_sat
5. Polydispersity effect: d = 2.0 ± 0.4 µm → 20% size variation → affects both magnetic content and drag; contributes to ν_c distribution within each batch
6. Conclusion: separation is not magnetically driven → must be DLVO

### 5.2 Transport Dynamics Close to the Surface

#### 5.2.1 Mean ensemble velocity

1. Experimental protocol: transport experiments for each particle type (COOH, NH₂) at 10+ frequencies spanning 0.5–25 Hz; H_x = 2.3 mT, H_z = 2.6 mT; 1000 fps, 5 s recordings
2. For each frequency and particle type: track all particles → filter trajectories (< 2000 frames, < 20 µm) → compute mean transport velocity per particle → average over all particles → mean ensemble velocity v̄(ν)
3. Present v(ν) curves for COOH and NH₂ side-by-side: linear regime v = νd at low ν, rollover at ν_c, decreasing velocity beyond
4. Fit v(ν) model (from Sec. 2.5.1) to extract ν_c as single free parameter: ν_c,COOH = 6.47 ± 0.11 Hz, ν_c,NH₂ = 4.29 ± 0.08 Hz (95% CI)
5. Separation ratio: ν_c,COOH / ν_c,NH₂ = 1.51 → significant, reproducible
6. Statistics: n_MP = 110–340 (COOH), 210–540 (NH₂); n_v = 2,900–270,000 velocity data points per measurement
7. Error analysis: 95% confidence intervals from nonlinear least squares; systematic uncertainties from pixel calibration, field calibration
8. Compare with Huhnstock Ch. 5: his COOH/NH₂ comparison showed only "marginal" mobility differences with 800 nm Si capping; this work's 700 nm polymer spacer produces clear separation
9. Interpret: higher ν_c for COOH → higher mobility → floating higher → less drag; lower ν_c for NH₂ → floating lower → more drag
10. Theoretical comparison: compute z_eq from DLVO force balance for both particle types → predict height difference → convert to ν_c ratio via Goldman drag → compare with measured ratio
11. Discuss: single-parameter fit quality — does the model describe the data well in both regimes? Show residuals or goodness-of-fit metric
12. IQR outlier removal: applied to velocity distributions at each frequency → removes stuck particles and measurement artifacts

**Figures**: v(ν) curves with fits for both particle types; histogram of velocities at selected frequencies; theoretical z_eq comparison

**Table**: ν_c values with 95% CI; number of particles; number of velocity data points per condition

#### 5.2.2 Steady-state velocity

1. Define: steady-state velocity = asymptotic velocity during a single transport step (not averaged over cycle)
2. Extraction: from position-time slope during the "flat" portion of a step (between acceleration and deceleration phases)
3. Frequency dependence: v_ss is approximately constant in phase-locked regime, decreases in phase-slipping
4. Compare COOH vs NH₂: at same frequency, v_ss is higher for COOH → consistent with ν_c interpretation
5. Relate to Goldman drag: v_ss = F_mag,x(z_eq) / f_D(z_eq)
6. Discuss: this metric provides a more direct measure of the drag force difference than the frequency-averaged velocity

### 5.3 Concluding remarks

1. Summary: demonstrated separation of identically-sized SPBs by surface chemistry through DLVO-mediated height-dependent drag
2. Quantify: ν_c,COOH / ν_c,NH₂ = 1.51 → factor of 1.5 difference in mobility
3. Mechanism: 10 mV ζ-potential difference → ~10–30 nm equilibrium height difference → significant drag change via Goldman correction
4. Comparison with Huhnstock: improved separation by using polymer spacer with matched ζ_s instead of Si/SiO₂
5. Implications for LOC: can sort particles by surface functionalization (e.g., analyte-bound vs. unbound) by choosing ν between ν_c,NH₂ and ν_c,COOH
6. Future: extend to physiological buffers; combine with focus pattern for spatial concentration

---

## Summary and Outlook

### Summary

1. Restate the research goal: quantify whether DLVO forces can enable surface-chemistry-based separation in traveling wave magnetophoresis
2. Summarize theory: DLVO framework predicts different equilibrium heights for different ζ potentials → Goldman-corrected drag → different ν_c
3. Summarize experimental design: Cu/IrMn/CoFe/Si layer stack + 700 nm polymer spacer + IBMP hh/tt pattern + trapezoidal fields at 4000 mT/s
4. Summarize tracking methodology: trackpy-based automated tracking with robust filtering criteria → large statistics (up to 540 particles, 270,000 velocity data points)
5. Key result: ν_c,COOH = 6.47 Hz vs. ν_c,NH₂ = 4.29 Hz → ratio 1.51; same χ (0.26 vs 0.27) → confirms DLVO origin
6. Comparison with predecessor work: Huhnstock found marginal COOH/NH₂ differences with Si capping; polymer spacer in this work amplifies the electrostatic differentiation
7. Supporting evidence: bulk χ measurement rules out magnetic force as separation mechanism

### Outlook

1. Extend to physiological buffers (PBS, cell culture media): higher ionic strength → shorter Debye length → reduced electrostatic differentiation → need to optimize spacer material/thickness
2. Protein-functionalized particles: BSA, streptavidin-biotin → analyte binding changes effective ζ → detect analyte presence via ν_c shift
3. Combine separation with spatial concentration: use Huhnstock's focus pattern + frequency tuning → concentrate sorted fractions at defined locations
4. 3D trajectory tracking: implement Huhnstock's TBG-based z-position measurement → directly verify predicted equilibrium height differences
5. Optimization: vary spacer thickness, material (PMMA, SiO₂, parylene) → tune separation efficiency
6. Two-dimensional transport: use checkerboard domain pattern for more complex sorting schemes
7. Integration into microfluidic chip: combine with inlet/outlet channels for continuous-flow separation
8. Tissue substrates: preliminary results on particle transport above biological tissue

---

## Abstract

1. Context: LOC devices for diagnostics rely on magnetic particle manipulation
2. Challenge: existing magnetophoretic separation methods use size/magnetization differences → cannot distinguish particles with identical magnetic properties but different surface chemistry
3. This work: demonstrates separation based on DLVO-mediated surface interactions in a traveling wave magnetophoresis system
4. System: IBMP-patterned EB thin film (Cu/IrMn/CoFe/Si) with hh/tt stripe domains and P(MMA-co-AA) polymer spacer
5. Principle: different ζ potentials → different equilibrium heights → different hydrodynamic drag → different critical transport frequencies
6. Key result: ν_c ratio of 1.51 between COOH and NH₂ functionalized 2 µm SPBs
7. Large-scale statistics: up to 540 particles and 270,000 velocity measurements per condition
8. Theoretical framework: single-parameter v(ν) model extracts ν_c from ensemble data
9. Significance: demonstrates surface-mediated particle sorting at the micrometer scale → pathway to analyte-specific detection in LOC systems
10. (Kurzfassung: German translation of above)
