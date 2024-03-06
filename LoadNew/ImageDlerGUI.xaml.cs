using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using WallpaperChanger.Shared;

namespace WallpaperChanger.LoadNew
{
    /// <summary>
    /// Interaction logic for ImageDlerGUI.xaml
    /// </summary>
    public partial class ImageDlerGUI : Window
    {
        private static int IMAGE_LOADING_BATCH = 10;

        ImageDler imageDler;
        WpcImageContainer imageContainer;
        List<WpcImage> loadedImages;
        int imageIndex;
        Thread bgLoader;
        public ImageDlerGUI(ImageDler imageDler, WpcImageContainer imageContainer)
        {
            this.imageDler = imageDler;
            this.imageContainer = imageContainer;
            loadedImages = new List<WpcImage>();
            imageIndex = 0;
            InitializeComponent();
        }

        private void LoadNewImages()
        {
            loadedImages.AddRange(imageDler.downloadImages(IMAGE_LOADING_BATCH));
        }

        private void UpdateButtonStates()
        {
            prev.IsEnabled = (imageIndex > 0);
            next.IsEnabled = (imageIndex < loadedImages.Count-1);
        }

        private void prev_Click(object sender, RoutedEventArgs e)
        {
            imageIndex--;
            AfterImageSwitch();
        }

        private void next_Click(object sender, RoutedEventArgs e)
        {
            imageIndex++;
            AfterImageSwitch();
        }

        private void AfterImageSwitch()
        {
            UpdateButtonStates();
            ShowImage();
            var restImages = loadedImages.Count - imageIndex;
            if(restImages < 5) { LoadNewImagesInBackground(); }
        }

        private void ShowImage()
        {
            image.Source = GetCurrentImage().asBitmapSource();
        }

        private WpcImage GetCurrentImage()
        {
            return loadedImages[imageIndex];
        }

        private void LoadNewImagesInBackground()
        {
            if (bgLoader != null && bgLoader.IsAlive) return;
            bgLoader = new Thread(LoadNewImages);
            bgLoader.Start();
        }

        private void save_Click(object sender, RoutedEventArgs e)
        {
            imageContainer.add(GetCurrentImage());
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            e.Cancel = true;
            Hide();
        }

        private void Window_IsVisibleChanged(object sender, DependencyPropertyChangedEventArgs e)
        {
            if (!IsVisible) return;
            if (loadedImages.Count == 0) LoadNewImages();
            ShowImage();
            UpdateButtonStates();
        }
    }
}
