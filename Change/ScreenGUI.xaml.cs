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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WallpaperChanger.Change
{
    /// <summary>
    /// Interaction logic for ScreenGUI.xaml
    /// </summary>
    public partial class ScreenGUI : UserControl
    {
        public event EventHandler<EventArgs> ChangeClicked;
        public Shared.Screen screen { get; private set; }
        public ScreenGUI(Shared.Screen screen)
        {
            InitializeComponent();
            this.screen = screen;
            LoadImage();
        }

        public void LoadImage()
        {
            if (screen.wpcImage == null) return;
            image.Source = screen.wpcImage.asBitmapSource();
        }

        private void changeBtn_Click(object sender, RoutedEventArgs e)
        {
            if (ChangeClicked != null) ChangeClicked(this, EventArgs.Empty);
        }
    }
}
