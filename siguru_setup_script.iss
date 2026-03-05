; ============================================================
;  SiGURU AI Assistant — Inno Setup Script
;  Versi: 1.1.0
;  CATATAN: Script ini mendistribusikan SELURUH folder dist/SiGURU_AI/
;           (hasil build --onedir), bukan satu file .exe tunggal.
; ============================================================

#define MyAppName "SiGURU AI Assistant"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "SiGURU AI"
#define MyAppURL "https://siguru.app"
#define MyAppExeName "SiGURU_AI.exe"
#define DistDir "d:\01. Punya Anggota\Akmal\AGENT\AI_Guru_Assistant\dist\SiGURU_AI"

[Setup]
AppId={{D3B7316A-9154-4E6D-AEC1-C8A8F2EDD6A1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Install ke Program Files
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes

; Tidak perlu admin jika data disimpan di APPDATA
; Uncomment baris berikut jika ingin install per-user (tanpa admin):
; PrivilegesRequired=lowest

; Output installer
OutputDir=d:\01. Punya Anggota\Akmal\AGENT\AI_Guru_Assistant\installer
OutputBaseFilename=SiGURU_Setup_v1.1.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; ── SELURUH folder hasil build --onedir ──────────────────────────────────────
; Ini meng-copy semua file di dist/SiGURU_AI/ ke folder instalasi
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; ── CATATAN: Data user (config, .env, .salt) ─────────────────────────────────
; TIDAK perlu di-copy di sini. File-file tersebut disimpan otomatis oleh
; aplikasi ke: C:\Users\[nama]\AppData\Roaming\SiGURU_AI\
; saat user menjalankan Setup Wizard pertama kali.

[Icons]
; Shortcut di Start Menu
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Shortcut di Desktop (opsional, user pilih di installer)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Jalankan aplikasi setelah install selesai
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Kosongkan folder log saat uninstall (data user di APPDATA dipertahankan)
Type: filesandordirs; Name: "{app}"
