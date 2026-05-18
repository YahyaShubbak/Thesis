from matplotlib import pyplot as plt
import numpy as np

# Debye length for a monovalent salt at 25 °C:
#   lambda_D = 3.04 Å / sqrt(c / (1 mol L^-1))
# where c is the salt concentration in mol L^-1.

#Fontsize to 18 for everythig:
plt.rcParams.update({
    "font.size": 18,
    "font.family": "serif",
    "font.serif": ["CMU Serif", "DejaVu Serif", "Computer Modern"],
    "text.usetex": True
})

def debye_length(concentration_mol_per_l):
    return 3.04e-10 / np.sqrt(concentration_mol_per_l)


def potential_decay(distance_m, psi0=50e-3, lambda_D=None):
    return psi0 * np.exp(-distance_m / lambda_D)


def main():
    concentrations = {
        r"1$\,$mM": 1e-3,
        r"10$\,$mM": 1e-2,
        r"0.1$\,$M": 1e-1,
    }

    x_nm = np.linspace(0, 10, 300)
    x_m = x_nm * 1e-9
    psi0 = 50e-3

    plt.figure(figsize=(7, 5))
    annotation_positions = {
        r"1$\,$mM": (3.0, 13),
        r"10$\,$mM": (4.0, 22),
        r"0.1$\,$M": (7.0, 40),
    }

    for label, c in concentrations.items():
        lambda_D = debye_length(c)
        psi = potential_decay(x_m, psi0=psi0, lambda_D=lambda_D)
        line, = plt.plot(x_nm, psi * 1e3, linewidth=2)

        x_annot, y_annot = annotation_positions[label]
        y_curve = potential_decay(x_annot * 1e-9, psi0=psi0, lambda_D=lambda_D) * 1e3
        plt.annotate(
            label,
            xy=(x_annot, y_curve),
            xytext=(x_annot + 1.2, y_curve + 6),
            textcoords="data",
            arrowprops=dict(arrowstyle="->", color=line.get_color(), lw=1.5),
            color=line.get_color(),
            fontsize=18,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="none"),
        )

    plt.xlabel(r"Distance $x$ / nm")
    plt.ylabel(r"Potential $\Psi$ / mV")
    # plt.title("Electrostatic potential decay for monovalent salt concentrations at 25 °C")
    plt.xlim(0, 10)
    plt.ylim(0, 50)
    plt.grid(True, linestyle="-", alpha=0.5)
    plt.tick_params(direction="in", which="both")
    plt.tight_layout()
    plt.savefig("Debye_length.png", dpi=300, bbox_inches="tight")
    plt.savefig("Debye_length.pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()

