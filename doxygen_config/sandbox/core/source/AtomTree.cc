#include <vector>

class AtomTree {

	public:

		AtomTree();
		~AtomTree();

		int size() {};
		int dof() {};
		int jump() {};

		void set_dof(int dof) {};
		void set_jump(int dof) {};

	private:
		vector<int> atoms_;
};

