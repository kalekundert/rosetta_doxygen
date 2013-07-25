class Energies {

	public:

		Energies();
		~Energies();

		double total_energy() { return total_energy_; }
		bool energies_updated() { return up_to_date_; }

	private:
		double total_energy_;
		bool up_to_date_;
};

