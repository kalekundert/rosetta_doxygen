#include <vector>

class FoldTree {

	public:

		FoldTree();
		~FoldTree();

		int size() {};
		void add_edge(int start, int stop) {};
		void remove_edge(int index) {};

	private:
		vector<int> edges_;
};

