using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Drawing;
using WallpaperChanger.Shared;
using System.Diagnostics;
using WallpaperChanger.Util;

namespace WallpaperChanger.Change
{
    /// <summary>
    /// Interaction logic for ChangerGUI.xaml
    /// </summary>
    public partial class ChangerGUI : Window
    {
        private static int SCREEN_MARGIN = 10;

        Changer changer;
        List<ScreenGUI> screenGUIs;
        SettingsGUI settingsGUI;

        public ChangerGUI(Changer changer)
        {
            InitializeComponent();
            this.changer = changer;
            screenGUIs = new List<ScreenGUI>();
            foreach(var screen in changer.screens)
            {
                var screenGUI = new ScreenGUI(screen);
                screenGUI.ChangeClicked += OnChangeClicked;
                screenGUIs.Add(screenGUI);
                screens.Children.Add(screenGUI);
            }
            settingsGUI = new SettingsGUI(changer);
            Logger.Debug(this, $"initialized. Width: {Width}; Height: {Height}");
        }

        private void OnChangeClicked(object? sender, EventArgs e)
        {
            if(sender == null) return;
            var screenGUI = (ScreenGUI)sender;
            changer.ChangeWallpaper(screenGUI.screen);
        }

        public void RefreshAllImages()
        {
            Dispatcher.Invoke(new Action(() =>
            {
                foreach (var screenGUI in screenGUIs)
                {
                    screenGUI.LoadImage();
                }
            }));
        }

        private void settings_Click(object sender, RoutedEventArgs e)
        {
            if (settingsGUI.IsVisible) return;
            settingsGUI.Show();
        }

        private void changeAll_Click(object sender, RoutedEventArgs e)
        {
            changer.ChangeAllWallpaper();
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            e.Cancel = true;
            Hide();
        }
    }
}
