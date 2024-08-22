{
	description = "Python dev env";
	inputs={
		nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
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
					python311Packages.pip
					python311Packages.tensorflow
					python311Packages.numpy
					python311Packages.pandas
					python311Packages.matplotlib
					python311Packages.scipy
					python311Packages.scikit-learn
					python311Packages.jupyterlab
					python311Packages.pytorch
					python311Packages.ipython        # Adiciona o IPython
					python311Packages.black          # Adiciona o Black para formatação
					python311Packages.flake8         # Adiciona Flake8 para verificação de sintaxe (Flycheck pode usá-lo)
					python311Packages.jedi           # Autocompletar e navegação de código
				];
			};
	};
}

