{
  description = "Advent of Code 2025";

  inputs.nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";

  outputs =
    { nixpkgs, ...}:
    let
      supportedSystems = [ "x86_64-linux" ];
      genConfig = (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          formatter.${system} = pkgs.nixfmt-tree;
          devShells.${system}.default = pkgs.mkShell { packages = [ pkgs.go ]; };
        }
      );
    in
    nixpkgs.lib.fold (result: next: nixpkgs.lib.recursiveUpdate result next) { } (
      map (system: genConfig system) supportedSystems
    );
}
