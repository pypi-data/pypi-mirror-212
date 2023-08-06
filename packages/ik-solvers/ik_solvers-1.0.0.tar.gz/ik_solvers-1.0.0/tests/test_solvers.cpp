#include <IKSolver.h>
#include <ForwardDynamicsSolver.h>
#include <urdf_parser/urdf_parser.h>
#include <kdl_parser.hpp>
#include <iostream>
int main(int argc, char** argv)
{
    std::vector<double> joint_limits_lower;
    std::vector<double> joint_limits_upper;
    for(int i = 0; i < 6; i++)
    {
        joint_limits_lower.push_back(-3.14);
        joint_limits_upper.push_back(3.14);
    }
    auto robot_model = urdf::parseURDFFile("ur10e.urdf");
    KDL::Chain robot_chain;
    KDL::Tree   robot_tree;
    kdl_parser::treeFromUrdfModel(*robot_model,robot_tree);
    std::shared_ptr<ik_solvers::IKSolver> ik_solver;
    std::vector<double> joint_pos;
    std::vector<double> joint_vel;
    for(int i = 0; i < 6; i++)
    {
        joint_pos.push_back(0);
        joint_vel.push_back(0);
    }
    ik_solver->setStartState(joint_pos, joint_vel);
    ik_solver->updateKinematics();
    
    ctrl::Vector6D cartesian_input = (ctrl::Vector6D() << 0, 0, 1, 0, 0, 0).finished();
    for(int i = 0; i < 10; i++)
    {
        auto ouput = ik_solver->getJointControlCmds(0.01, cartesian_input);
        ik_solver->updateKinematics();
    }
    
    
    return 0;
}