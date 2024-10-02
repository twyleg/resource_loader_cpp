// Copyright (C) 2024 twyleg
#include <gtest/gtest.h>

#include <resource_loader.h>

namespace resource_loader_generator::Testing {

class ResourceLoaderTest : public ::testing::Test {

public:

	ResourceLoaderTest()
	{}

	void SetUp() override {
		// Do stuff
	}

protected:

};

TEST_F(ResourceLoaderTest, InitialState_Action_Expectation)
{
	EXPECT_EQ(ResourceLoader::getResourceAsString("example_resource_one.txt"), "example resource \"one\" from app\n");
}

}