{ pkgs ? import <nixpkgs> {} }:

let
  # Create a python environment with the required packages
  myPythonEnv = pkgs.python313.withPackages (ps: with ps; [
    pygame  # The library for game/audio/main logic
    pillow  # For image handling (PIL)
    nuitka  # The compiler for your portable binary
    pyinstaller # Compile python to exe
  ]);
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    myPythonEnv

    # System dependencies for Pygame/Audio
    zlib
    glib
    alsa-lib
    SDL2
    SDL2_mixer

    # Tool for making binaries portable later
    patchelf
  ];

  # Important: NixOS specific hook to help Pygame find libraries at runtime
  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.glib pkgs.zlib pkgs.alsa-lib pkgs.SDL2 pkgs.SDL2_mixer ]}:$LD_LIBRARY_PATH"
  '';
}
