
#define MyAppName "SkyCast"
#define MyAppVersion "1.0.0"

[Setup]
AppId=SkyCastWeatherApp
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={localappdata}\Programs\SkyCast
DefaultGroupName=SkyCast
PrivilegesRequired=lowest
OutputDir=installer_output
OutputBaseFilename=SkyCastSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\SkyCast.exe

[Files]
Source: "dist\SkyCast\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Icons]
Name: "{group}\SkyCast"; Filename: "{app}\SkyCast.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\SkyCast"; Filename: "{app}\SkyCast.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\SkyCast.exe"; Description: "Launch SkyCast"; Flags: nowait postinstall skipifsilent
