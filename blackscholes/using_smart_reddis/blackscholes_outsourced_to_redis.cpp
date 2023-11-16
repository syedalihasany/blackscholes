#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <iomanip>
#include <chrono>
#include <sstream>
#include <stdlib.h>
// including the redis client header
#include "client.h"


int main(int argc, char* argv[]) {
    std::cout<<"start"<<std::endl;
    // Set environment variables
    setenv("SR_LOG_FILE", "smartredis.log", 1);
    setenv("SR_LOG_LEVEL", "INFO", 1);
    setenv("SSDB", "localhost:6379", 1); // Adjust the address and port as needed
    

    // initializing redis server through command line 
    //int status = system("redis-server");
    // Create a ConfigOptions object
    //SmartRedis::ConfigOptions config_options;
    //config_options.set_redis_server_type(SmartRedis::Server_Type::SSDB);


    // Initialize a vector that will hold the input tensor
    size_t n_rows = 1000;
    size_t n_cols = 6;
    size_t n_values = n_rows * n_cols;
    std::vector<float> input_tensor(n_values, 0);
    std::vector<size_t> dims = {1000, 6};
    
    // Read values from the tab separated input feature file
    std::string input_file = "../input_features.txt";
    std::ifstream file(input_file);
    std::cout<<"after inputs"<<std::endl;
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << input_file << std::endl;
        return 1;
    }

    for (size_t row = 0; row < n_rows; row++) {
        for (size_t col = 0; col < n_cols; col++) {
            float value;
            if (col < n_cols - 1) {
                file >> value;
                file.ignore(1); // Skip the tab character
            } else {
                file >> value;
            }
            input_tensor[row * n_cols + col] = value; // makes the 100k by 6 into a linear tensor
        }
    }

    file.close();

    // Initialize a SmartRedis client
    bool cluster_mode = false; // Set to false if not using a clustered database
    SmartRedis::Client client(cluster_mode, __FILE__);
    std::cout<<"set client"<<std::endl;

    // Use the client to set a model in the database from a file
    std::string model_key = "ali_model";
    std::string model_file = "../ali_model_scripted.pt";
    std::cout<<"USING CPU"<<std::endl;
    client.set_model_from_file(model_key, model_file, "TORCH", "CPU",1000); // the last parameter is the batch size should we pass this as 100k
    std::cout<<"set model"<<std::endl;

    // Declare keys that we will use in forthcoming client commands
    std::string in_key = "input_key";
    std::string out_key = "output_key";

    // Put the tensor into the database that was loaded from file
    client.put_tensor(in_key, input_tensor.data(), dims, SRTensorTypeFloat, SRMemLayoutNested);

    // running the model 
    client.run_model(model_key, {in_key}, {out_key});

    // assigning the dimensions of the output tensor to the output_dims vector
    std::vector<size_t> output_dims = {1000, 1};

    std::vector<float> result(1000, 0);
    client.unpack_tensor(out_key, result.data(), output_dims,SRTensorTypeFloat, SRMemLayoutNested);


    // Create an output file stream
    std::ofstream outputFile("./ali_model_results_using_Cpp_and_Redis.txt");

    if (outputFile.is_open()) {
        for (size_t i = 0; i < result.size(); i++) {
            outputFile << result[i] << std::endl;
    }
        outputFile.close();
    } else {
        std::cerr << "Error: Unable to open the output file." << std::endl;
    }



    return 0;
}
