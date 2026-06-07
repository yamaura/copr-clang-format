# Build only the clang-format tool out of LLVM/Clang, as a statically linked
# binary installed as /usr/bin/clang-format-21 (coexists with the distro clang).

Name:           clang-format-21
Version:        21.1.8
Release:        1%{?dist}
Summary:        Standalone, statically linked clang-format from LLVM 21

License:        Apache-2.0 WITH LLVM-exception
URL:            https://github.com/llvm/llvm-project
Source0:        %{url}/releases/download/llvmorg-%{version}/llvm-%{version}.src.tar.xz
Source1:        %{url}/releases/download/llvmorg-%{version}/clang-%{version}.src.tar.xz
# Since LLVM 15 the per-project tarballs no longer bundle the shared CMake
# modules; llvm/clang reference them at ../cmake, so this must be unpacked too.
Source2:        %{url}/releases/download/llvmorg-%{version}/cmake-%{version}.src.tar.xz

# A fully static binary carries no shared-library symbols, so there is no
# debuginfo to extract and no .so to ldconfig.
%define debug_package %{nil}

BuildRequires:  cmake >= 3.20.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  xz
# needed to link -static
BuildRequires:  glibc-static
BuildRequires:  libstdc++-static

%description
clang-format reformats C/C++/Java/JavaScript/JSON/Objective-C/Protobuf/C#
source according to a configurable style. This package provides the
clang-format tool from LLVM/Clang %{version}, built as a self-contained
statically linked executable named clang-format-21.

%prep
rm -rf llvm clang cmake build
tar -xf %{SOURCE0}
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
mv llvm-%{version}.src  llvm
mv clang-%{version}.src clang
# llvm/clang expect the shared CMake modules as a sibling directory named cmake
mv cmake-%{version}.src cmake

%build
cmake -G Ninja -S llvm -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DLLVM_ENABLE_PROJECTS=clang \
    -DLLVM_TARGETS_TO_BUILD=X86 \
    -DBUILD_SHARED_LIBS=OFF \
    -DLLVM_BUILD_LLVM_DYLIB=OFF \
    -DLLVM_LINK_LLVM_DYLIB=OFF \
    -DLLVM_ENABLE_PIC=OFF \
    -DLLVM_BUILD_TOOLS=OFF \
    -DLLVM_INCLUDE_TESTS=OFF \
    -DLLVM_INCLUDE_EXAMPLES=OFF \
    -DLLVM_INCLUDE_BENCHMARKS=OFF \
    -DLLVM_ENABLE_ZLIB=OFF \
    -DLLVM_ENABLE_ZSTD=OFF \
    -DLLVM_ENABLE_LIBXML2=OFF \
    -DLLVM_ENABLE_LIBEDIT=OFF \
    -DCLANG_ENABLE_STATIC_ANALYZER=OFF \
    -DCLANG_ENABLE_ARCMT=OFF \
    -DCMAKE_EXE_LINKER_FLAGS="-static -static-libgcc -static-libstdc++"

cmake --build build --target clang-format

%install
install -D -m0755 build/bin/clang-format %{buildroot}%{_bindir}/clang-format-21
strip %{buildroot}%{_bindir}/clang-format-21

%check
# Confirm the produced binary is actually static and runs.
file %{buildroot}%{_bindir}/clang-format-21
%{buildroot}%{_bindir}/clang-format-21 --version

%files
%license llvm/LICENSE.TXT
%{_bindir}/clang-format-21

%changelog
* Sat Jun 06 2026 Yuki Yamaura <yamaura@pezy.co.jp> 21.1.8-1
- Initial package: standalone static clang-format from LLVM 21.1.8
