{
  description = "FHS development environment for CV training";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        
        # Create an FHS environment
        fhs = pkgs.buildFHSEnv {
          name = "cv-training-env";
          
          # Packages needed in the FHS environment
          targetPkgs = pkgs: with pkgs; [
            uv
            ruff
            python313
            python313Packages.pip
            python313Packages.virtualenv
            
            # This provides libstdc++.so.6
            stdenv.cc.cc.lib
            
            # Other common dependencies for Python C-extensions
            zlib
            glib
            libGL
            
            # OpenCV GUI dependencies
            libX11
            libXext
            libXrender
            libICE
            libSM
            libxcb
            gtk3
            qt5.qtbase
          ];
          
          # Command to run when entering the shell
          runScript = "bash";
        };
      in
      {
        devShells.default = fhs.env;
      }
    );
}
