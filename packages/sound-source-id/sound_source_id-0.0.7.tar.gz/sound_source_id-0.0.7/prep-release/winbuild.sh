#!/bin/sh

rm -r ../windows_installer/sound_source_id_for_win
mkdir ../windows_installer/sound_source_id_for_win
mkdir ../windows_installer/sound_source_id_for_win/doc
mkdir ../windows_installer/sound_source_id_for_win/prm_files

wine cmd /c "Z:\media\ntfsShared\lin_home\auditory\code\sound_source_id\prep-release\winbuild.bat"

rsync -rtv ../build/exe.win-amd64-3.11/ ../windows_installer/sound_source_id_for_win/
rsync -rtv ../build/exe.win-amd64-3.11/lib/sound_source_id/doc/ ../windows_installer/sound_source_id_for_win/doc/
rsync -rtv ../build/exe.win-amd64-3.11/lib/sound_source_id/prm_files/ ../windows_installer/sound_source_id_for_win/prm_files/
#cp -r ../build/exe.win-amd64-3.11/* ../windows_installer/sound_source_id_for_win/
#cp -r ../build/exe.win-amd64-3.11/lib/sound_source_id/doc/ ../windows_installer/sound_source_id_for_win/doc/
#cp -r ../build/exe.win-amd64-3.11/lib/sound_source_id/prm_files/* ../windows_installer/sound_source_id_for_win/prm_files/

wine cmd /c "Z:\media\ntfsShared\lin_home\auditory\code\sound_source_id\prep-release\win_compile_installer.bat"
