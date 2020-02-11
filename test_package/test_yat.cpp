#include <iostream>
#include <yat/Version.h>

int main() {
    std::cout << yat::Version::get() << std::endl;
    return 0;
}
