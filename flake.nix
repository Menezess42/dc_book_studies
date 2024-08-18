{
  description = "Ambiente Python com nix-flakes";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShells = {
      default = nixpkgs.lib.mkShell {
        buildInputs = [
          nixpkgs.python310
          nixpkgs.python310Packages.pip
          nixpkgs.python310Packages.numpy
          nixpkgs.python310Packages.pandas
        ];

        shellHook = ''
          echo "Ambiente Python com nix-flakes ativado!"
        '';
      };
    };
  };
}

