{
	description = "Python dev env";
	inputs={
		nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    #emacs-config.url = "path:~/.emacs.d/config/emacs_pyIDE.nix";
	};
	outputs = {self, nixpkgs, ...}@inputs:
	let
		system = "x86_64-linux";
	pkgs=nixpkgs.legacyPackages.${system};
	in
	{
		devShells.${system}.default=
			pkgs.mkShell
			{
				nativeBuildInputs = with pkgs; [
					python311
          python311Packages.beautifulsoup4
          python311Packages.html5lib
          python311Packages.requests
					python311Packages.pip
					python311Packages.tensorflow
					python311Packages.numpy
					python311Packages.pandas
					python311Packages.matplotlib
					python311Packages.scipy
					python311Packages.scikit-learn
					python311Packages.jupyterlab
					python311Packages.pytorch
					python311Packages.ipython
# Emacs pyIDE libs
				python311Packages.jedi
				python311Packages.black
				python311Packages.flake8
				python311Packages.sentinel
				python311Packages.python-lsp-server
				python311Packages.virtualenv
				python311Packages.pyflakes  # Linter Pyflakes
				direnv
				];
			};
	};
}

