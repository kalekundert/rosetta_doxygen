class Pose {

	public:

		Pose();
		~Pose();

		FoldTree fold_tree() { return fold_tree_; }
		AtomTree atom_tree() { return atom_tree_; }
		Energies energies() { return energies_; }

	private:
		FoldTree fold_tree_;
		AtomTree atom_tree_;
		Energies energies_;
};

