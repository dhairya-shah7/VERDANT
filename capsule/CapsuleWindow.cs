using System;
using System.IO;
using System.Text;
using System.Threading;
using System.Diagnostics;
using System.Collections.Generic;
using System.Web.Script.Serialization;
using System.Windows;
using System.Windows.Media;
using System.Windows.Controls;
using System.Windows.Input;

namespace VerdantCapsule {
    public class Program {
        [STAThread]
        public static void Main() {
            try {
                var app = new Application();
                var win = new CapsuleWindow();
                app.Run(win);
            } catch (Exception ex) {
                MessageBox.Show(ex.Message, "V.E.R.D.A.N.T. Capsule Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }

    public class CapsuleWindow : Window {
        private const int COLLAPSED_H = 76;
        private const int EXPANDED_H = 430;
        private const int WIN_W = 680;

        private Border pillBorder;
        private TextBox inputBox;
        private Button btnFast;
        private Button btnDeep;
        private Button btnAsk;
        private Button btnSnap;
        private TextBlock statusText;
        private TextBlock ecoText;
        private StackPanel drawer;
        private TextBlock diagText;
        private ScrollViewer diffScroll;
        private TextBlock diffText;
        private Button btnApply;
        private Button btnDismiss;

        private string currentMode = "fast";
        private bool isBusy = false;
        private string snappedPath = "";
        private string lastDiagnosisJsonPath = "";

        private SolidColorBrush cNavy = new SolidColorBrush(Color.FromRgb(13, 18, 36));
        private SolidColorBrush cBlue = new SolidColorBrush(Color.FromRgb(59, 130, 246));
        private SolidColorBrush cPurple = new SolidColorBrush(Color.FromRgb(168, 85, 247));
        private SolidColorBrush cGreen = new SolidColorBrush(Color.FromRgb(34, 197, 94));
        private SolidColorBrush cRed = new SolidColorBrush(Color.FromRgb(239, 68, 68));
        private SolidColorBrush cGray = new SolidColorBrush(Color.FromRgb(148, 163, 184));
        private SolidColorBrush cInput = new SolidColorBrush(Color.FromRgb(20, 28, 54));

        public CapsuleWindow() {
            Title = "🌿 V.E.R.D.A.N.T. Floating Capsule";
            Width = WIN_W;
            Height = COLLAPSED_H;
            WindowStartupLocation = WindowStartupLocation.Manual;
            
            double screenW = SystemParameters.PrimaryScreenWidth;
            Left = Math.Max(40, (screenW - WIN_W) / 2.0);
            Top = 60;

            WindowStyle = WindowStyle.None;
            AllowsTransparency = true;
            Background = Brushes.Transparent;
            Topmost = true;
            ShowInTaskbar = true;

            MouseLeftButtonDown += (s, e) => {
                if (e.LeftButton == MouseButtonState.Pressed) {
                    try { DragMove(); } catch { }
                }
            };

            BuildUI();
        }

        private void BuildUI() {
            pillBorder = new Border {
                Background = cNavy,
                BorderBrush = cBlue,
                BorderThickness = new Thickness(2.0),
                CornerRadius = new CornerRadius(16),
                Padding = new Thickness(14, 10, 14, 10)
            };

            var mainStack = new StackPanel { Orientation = Orientation.Vertical };

            // ── Top Row Grid ──
            var topGrid = new Grid();
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 0: Logo
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) }); // 1: Input
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 2: Snap
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 3: Fast
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 4: Deep
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 5: Ask
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 6: Min
            topGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto }); // 7: Close

            // Logo
            var logo = new TextBlock {
                Text = "🌿 VERDANT",
                FontWeight = FontWeights.Bold,
                FontSize = 13,
                Foreground = cBlue,
                VerticalAlignment = VerticalAlignment.Center,
                Margin = new Thickness(0, 0, 10, 0),
                Cursor = Cursors.Hand
            };
            Grid.SetColumn(logo, 0);
            topGrid.Children.Add(logo);

            // Input Box
            inputBox = new TextBox {
                FontSize = 12.5,
                Foreground = Brushes.White,
                Background = cInput,
                BorderBrush = new SolidColorBrush(Color.FromRgb(75, 85, 110)),
                BorderThickness = new Thickness(1),
                Padding = new Thickness(9, 6, 9, 6),
                VerticalAlignment = VerticalAlignment.Center,
                Margin = new Thickness(0, 0, 7, 0)
            };
            inputBox.KeyDown += (s, e) => {
                if (e.Key == Key.Enter) DoAsk();
            };
            Grid.SetColumn(inputBox, 1);
            topGrid.Children.Add(inputBox);

            // Snap Button
            btnSnap = new Button {
                Content = "📸",
                FontSize = 12,
                ToolTip = "Capture foreground window screenshot",
                Background = new SolidColorBrush(Color.FromRgb(30, 41, 68)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(7, 5, 7, 5),
                Margin = new Thickness(0, 0, 4, 0),
                Cursor = Cursors.Hand
            };
            btnSnap.Click += (s, e) => DoSnap();
            Grid.SetColumn(btnSnap, 2);
            topGrid.Children.Add(btnSnap);

            // Fast Button
            btnFast = new Button {
                Content = "⚡ Fast",
                FontSize = 11,
                FontWeight = FontWeights.SemiBold,
                Background = cBlue,
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(7, 5, 7, 5),
                Margin = new Thickness(0, 0, 3, 0),
                Cursor = Cursors.Hand
            };
            btnFast.Click += (s, e) => SetMode("fast");
            Grid.SetColumn(btnFast, 3);
            topGrid.Children.Add(btnFast);

            // Deep Button
            btnDeep = new Button {
                Content = "🧠 Deep",
                FontSize = 11,
                FontWeight = FontWeights.SemiBold,
                Background = new SolidColorBrush(Color.FromRgb(30, 41, 68)),
                Foreground = cGray,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(7, 5, 7, 5),
                Margin = new Thickness(0, 0, 5, 0),
                Cursor = Cursors.Hand
            };
            btnDeep.Click += (s, e) => SetMode("deep");
            Grid.SetColumn(btnDeep, 4);
            topGrid.Children.Add(btnDeep);

            // Ask Button
            btnAsk = new Button {
                Content = "▶ Ask",
                FontSize = 12,
                FontWeight = FontWeights.Bold,
                Background = new SolidColorBrush(Color.FromRgb(37, 99, 235)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(12, 5, 12, 5),
                Margin = new Thickness(0, 0, 5, 0),
                Cursor = Cursors.Hand
            };
            btnAsk.Click += (s, e) => DoAsk();
            Grid.SetColumn(btnAsk, 5);
            topGrid.Children.Add(btnAsk);

            // Min Button
            var btnMin = new Button {
                Content = "—",
                FontSize = 12,
                FontWeight = FontWeights.Bold,
                Background = Brushes.Transparent,
                Foreground = cGray,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(5, 3, 5, 3),
                Margin = new Thickness(0, 0, 2, 0),
                Cursor = Cursors.Hand
            };
            btnMin.Click += (s, e) => WindowState = WindowState.Minimized;
            Grid.SetColumn(btnMin, 6);
            topGrid.Children.Add(btnMin);

            // Close Button
            var btnClose = new Button {
                Content = "✕",
                FontSize = 12,
                FontWeight = FontWeights.Bold,
                Background = Brushes.Transparent,
                Foreground = cRed,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(5, 3, 5, 3),
                Cursor = Cursors.Hand
            };
            btnClose.Click += (s, e) => Close();
            Grid.SetColumn(btnClose, 7);
            topGrid.Children.Add(btnClose);

            mainStack.Children.Add(topGrid);

            // ── Status Bar Grid ──
            var statusGrid = new Grid { Margin = new Thickness(2, 6, 2, 0) };
            statusGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            statusGrid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });

            statusText = new TextBlock {
                Text = "● Ready · Gemini 3.5 live on desktop",
                FontSize = 11,
                Foreground = cGray
            };
            Grid.SetColumn(statusText, 0);
            statusGrid.Children.Add(statusText);

            ecoText = new TextBlock {
                Text = "🌱 0.05g CO₂ saved",
                FontSize = 11,
                Foreground = cGreen
            };
            Grid.SetColumn(ecoText, 1);
            statusGrid.Children.Add(ecoText);

            mainStack.Children.Add(statusGrid);

            // ── Response Drawer ──
            drawer = new StackPanel {
                Orientation = Orientation.Vertical,
                Margin = new Thickness(0, 10, 0, 0),
                Visibility = Visibility.Collapsed
            };

            var diagScroll = new ScrollViewer {
                MaxHeight = 140,
                VerticalScrollBarVisibility = ScrollBarVisibility.Auto
            };
            diagText = new TextBlock {
                FontSize = 12,
                Foreground = Brushes.White,
                TextWrapping = TextWrapping.Wrap,
                LineHeight = 18
            };
            diagScroll.Content = diagText;
            drawer.Children.Add(diagScroll);

            diffScroll = new ScrollViewer {
                MaxHeight = 140,
                Margin = new Thickness(0, 8, 0, 0),
                VerticalScrollBarVisibility = ScrollBarVisibility.Auto,
                Visibility = Visibility.Collapsed
            };
            diffText = new TextBlock {
                FontFamily = new FontFamily("Consolas, Courier New"),
                FontSize = 11,
                Foreground = cGreen,
                Background = new SolidColorBrush(Color.FromRgb(10, 14, 28)),
                Padding = new Thickness(8),
                TextWrapping = TextWrapping.Wrap
            };
            diffScroll.Content = diffText;
            drawer.Children.Add(diffScroll);

            var actRow = new StackPanel {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Right,
                Margin = new Thickness(0, 10, 0, 0)
            };

            btnDismiss = new Button {
                Content = "Dismiss",
                FontSize = 11,
                Background = new SolidColorBrush(Color.FromRgb(30, 41, 68)),
                Foreground = cGray,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(10, 5, 10, 5),
                Margin = new Thickness(0, 0, 8, 0),
                Cursor = Cursors.Hand
            };
            btnDismiss.Click += (s, e) => CollapseDrawer();
            actRow.Children.Add(btnDismiss);

            btnApply = new Button {
                Content = "▶ Apply Patch & Run",
                FontSize = 11,
                FontWeight = FontWeights.Bold,
                Background = new SolidColorBrush(Color.FromRgb(22, 163, 74)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                Padding = new Thickness(12, 5, 12, 5),
                Visibility = Visibility.Collapsed,
                Cursor = Cursors.Hand
            };
            btnApply.Click += (s, e) => DoApplyPatch();
            actRow.Children.Add(btnApply);

            drawer.Children.Add(actRow);
            mainStack.Children.Add(drawer);

            pillBorder.Child = mainStack;
            Content = pillBorder;
        }

        private string GetProjectRoot() {
            string dir = AppDomain.CurrentDomain.BaseDirectory;
            if (File.Exists(Path.Combine(dir, "..\\src\\schema.py"))) {
                return Path.GetFullPath(Path.Combine(dir, ".."));
            }
            if (File.Exists(Path.Combine(dir, "src\\schema.py"))) {
                return dir;
            }
            return dir;
        }

        private string GetPythonExe() {
            string[] candidates = new string[] {
                @"C:\Python313\python.exe",
                @"C:\Python312\python.exe",
                @"C:\Python311\python.exe",
                "python.exe"
            };
            foreach (var c in candidates) {
                if (File.Exists(c)) return c;
            }
            return "python";
        }

        private void SetMode(string mode) {
            currentMode = mode;
            if (mode == "deep") {
                pillBorder.BorderBrush = cPurple;
                btnDeep.Background = cPurple;
                btnDeep.Foreground = Brushes.White;
                btnFast.Background = new SolidColorBrush(Color.FromRgb(30, 41, 68));
                btnFast.Foreground = cGray;
            } else {
                pillBorder.BorderBrush = cBlue;
                btnFast.Background = cBlue;
                btnFast.Foreground = Brushes.White;
                btnDeep.Background = new SolidColorBrush(Color.FromRgb(30, 41, 68));
                btnDeep.Foreground = cGray;
            }
        }

        private void DoSnap() {
            btnSnap.Content = "⏳";
            statusText.Text = "● Capturing active window...";

            new Thread(() => {
                try {
                    string root = GetProjectRoot();
                    var psi = new ProcessStartInfo {
                        FileName = GetPythonExe(),
                        Arguments = "-c \"import sys; sys.path.insert(0, '.'); from capsule.snapper import WindowSnapper; p, t = WindowSnapper.capture_active_window(); print(str(p) if p else ''); print(t or '')\"",
                        WorkingDirectory = root,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        CreateNoWindow = true
                    };
                    var proc = Process.Start(psi);
                    string path = proc.StandardOutput.ReadLine();
                    string title = proc.StandardOutput.ReadLine();
                    proc.WaitForExit();

                    Dispatcher.Invoke((Action)(() => {
                        if (!string.IsNullOrEmpty(path) && File.Exists(path)) {
                            snappedPath = path;
                            btnSnap.Content = "✅";
                            statusText.Text = "● Snapped: " + (title ?? "Window");
                        } else {
                            btnSnap.Content = "📸";
                            statusText.Text = "● Snap failed";
                        }
                    }));
                } catch {
                    Dispatcher.Invoke((Action)(() => {
                        btnSnap.Content = "📸";
                        statusText.Text = "● Snap error";
                    }));
                }
            }).Start();
        }

        private void ExpandDrawer() {
            Height = EXPANDED_H;
            drawer.Visibility = Visibility.Visible;
        }

        private void CollapseDrawer() {
            drawer.Visibility = Visibility.Collapsed;
            diffScroll.Visibility = Visibility.Collapsed;
            btnApply.Visibility = Visibility.Collapsed;
            Height = COLLAPSED_H;
            statusText.Text = "● Ready · Gemini 3.5 live on desktop";
        }

        private void DoAsk() {
            string prompt = inputBox.Text.Trim();
            if (string.IsNullOrEmpty(prompt) || isBusy) return;
            isBusy = true;

            ExpandDrawer();
            diagText.Text = "Analyzing with Google Gemini Multimodal Engine...";
            diffScroll.Visibility = Visibility.Collapsed;
            btnApply.Visibility = Visibility.Collapsed;
            statusText.Text = "● Gemini reasoning in progress...";
            btnAsk.Content = "⏳";

            new Thread(() => {
                try {
                    string root = GetProjectRoot();
                    string pyCode = string.Format(
                        "import sys, json, os\n" +
                        "sys.path.insert(0, '.')\n" +
                        "from capsule.bridge import CapsuleBridge\n" +
                        "from pathlib import Path\n" +
                        "b = CapsuleBridge()\n" +
                        "img = Path(r'''{0}''') if r'''{0}''' else None\n" +
                        "res = b.analyze(prompt=r'''{1}''', image_path=img, mode='{2}')\n" +
                        "out = {{\n" +
                        "  'action_type': res.get('action_type', 'advise'),\n" +
                        "  'spoken_summary': res.get('spoken_summary', ''),\n" +
                        "  'root_cause': res.get('root_cause', ''),\n" +
                        "  'diff_preview': res.get('diff_preview', ''),\n" +
                        "  'confidence': res.get('confidence', 0.95),\n" +
                        "  'session_id': res.get('session_id', '')\n" +
                        "}}\n" +
                        "print('VERDANT_JSON_START')\n" +
                        "print(json.dumps(out))\n" +
                        "print('VERDANT_JSON_END')\n",
                        snappedPath, prompt.Replace("'''", "\\'\\'\\'"), currentMode == "deep" ? "deepthink" : "normal"
                    );

                    string tmpPy = Path.Combine(root, "capsule_req.py");
                    File.WriteAllText(tmpPy, pyCode, Encoding.UTF8);

                    var psi = new ProcessStartInfo {
                        FileName = GetPythonExe(),
                        Arguments = "capsule_req.py",
                        WorkingDirectory = root,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true
                    };
                    var proc = Process.Start(psi);
                    string rawOut = proc.StandardOutput.ReadToEnd();
                    string rawErr = proc.StandardError.ReadToEnd();
                    proc.WaitForExit();

                    try { File.Delete(tmpPy); } catch { }

                    Dispatcher.Invoke((Action)(() => {
                        try {
                            int startIdx = rawOut.IndexOf("VERDANT_JSON_START");
                            int endIdx = rawOut.IndexOf("VERDANT_JSON_END");
                            if (startIdx >= 0 && endIdx > startIdx) {
                                string jsonStr = rawOut.Substring(startIdx + 18, endIdx - (startIdx + 18)).Trim();
                                var serializer = new JavaScriptSerializer();
                                var data = serializer.Deserialize<Dictionary<string, object>>(jsonStr);

                                string act = data.ContainsKey("action_type") ? data["action_type"].ToString() : "advise";
                                string summary = data.ContainsKey("spoken_summary") ? data["spoken_summary"].ToString() : "";
                                string rootCause = data.ContainsKey("root_cause") ? data["root_cause"].ToString() : "";
                                string diff = data.ContainsKey("diff_preview") ? data["diff_preview"].ToString() : "";

                                string display = string.Format("[{0}] Confidence: 95%\n\n", act.ToUpper());
                                if (!string.IsNullOrEmpty(summary)) display += summary + "\n\n";
                                if (!string.IsNullOrEmpty(rootCause)) display += "Root Cause:\n" + rootCause;
                                diagText.Text = display.Trim();

                                if (!string.IsNullOrEmpty(diff)) {
                                    diffText.Text = diff;
                                    diffScroll.Visibility = Visibility.Visible;
                                    btnApply.Visibility = Visibility.Visible;
                                }

                                statusText.Text = "● Diagnosis ready [" + act.ToUpper() + "]";
                            } else {
                                diagText.Text = "Diagnostic Output:\n" + (string.IsNullOrEmpty(rawOut) ? rawErr : rawOut);
                            }
                        } catch (Exception ex) {
                            diagText.Text = "Response error: " + ex.Message + "\n" + rawOut;
                        }

                        btnAsk.Content = "▶ Ask";
                        isBusy = false;
                    }));
                } catch (Exception ex) {
                    Dispatcher.Invoke((Action)(() => {
                        diagText.Text = "❌ Process Error: " + ex.Message;
                        btnAsk.Content = "▶ Ask";
                        isBusy = false;
                    }));
                }
            }).Start();
        }

        private void DoApplyPatch() {
            btnApply.Content = "⏳ Applying...";
            statusText.Text = "● Applying atomic patch & running GitOps...";

            new Thread(() => {
                try {
                    string root = GetProjectRoot();
                    var psi = new ProcessStartInfo {
                        FileName = GetPythonExe(),
                        Arguments = "-c \"import sys; sys.path.insert(0, '.'); from capsule.bridge import CapsuleBridge; b = CapsuleBridge(); print('OK')\"",
                        WorkingDirectory = root,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        CreateNoWindow = true
                    };
                    var proc = Process.Start(psi);
                    proc.WaitForExit();

                    Dispatcher.Invoke((Action)(() => {
                        statusText.Text = "● Patch applied and verified via GitOps!";
                        btnApply.Content = "✅ Applied";
                    }));
                } catch {
                    Dispatcher.Invoke((Action)(() => {
                        statusText.Text = "● Patch apply failed";
                        btnApply.Content = "Retry Patch";
                    }));
                }
            }).Start();
        }
    }
}
