/// \example pose_from_pdb.cc

// Core headers
#include <core/pose/Pose.hh>
#include <core/import_pose/import_pose.hh>

// Utility headers
#include <devel/init.hh>
#include <basic/options/option.hh>
#include <basic/options/option_macros.hh>

// This program demonstrates three things:
// 1. How to create a pose from a PDB file.
// 2. How to create a PDB file from a pose.
// 3. How to add one-off command-line options to your applications.

using namespace std;
using namespace basic::options;

OPT_2GRP_KEY(File, examples, in, pdb)
OPT_2GRP_KEY(File, examples, out, pdb)

int main(int argc, char** argv) {
	NEW_OPT(examples::in, "Input PDB file", "");
	NEW_OPT(examples::out, "Output data file", "");

	// Parse command-line arguments and initialize Rosetta.
	devel::init(argc, argv);

	// Build a pose from the given PDB file.
	core::pose::Pose pose;
	core::import_pose::pose_from_pdb(pose, option[OptionKeys::examples::in]());

	// Write the pose to the given PDB file.
	pose.dump_pdb(option[OptionKeys::examples::out]());
}
