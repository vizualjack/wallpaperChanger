using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Forms;
using WallpaperChanger.Change;
using WallpaperChanger.LoadNew;
using WallpaperChanger.Shared;
using WallpaperChanger.Util;

namespace WallpaperChanger
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : System.Windows.Application
    {
        System.Windows.Forms.NotifyIcon trayIcon;
        WpcImageContainer imageContainer;
        Changer changer;
        ImageDler imageDler;
        Persister persister;
        List<Shared.Screen> screens;
        bool running = false;
        bool blackMode = false;
        Thread worker, tiWorker;

        public App()
        {
            screens = new List<Shared.Screen>();
            foreach (var wScreen in System.Windows.Forms.Screen.AllScreens)
            {
                screens.Add(new Shared.Screen(wScreen.Bounds.Width, wScreen.Bounds.Height));
            }
            persister = new Persister(WallpaperChanger.Resources.PERSISTER_PATH);
            imageContainer = new WpcImageContainer(WallpaperChanger.Resources.IMAGE_FOLDER);
            changer = new Changer(imageContainer, screens);
            var screen = screens[0];
            imageDler = new ImageDler(imageContainer, new WpcImage.Size(screen.width, screen.height));
            persister.Load(changer);
            persister.Load(imageDler);
            TrayIcon();
            StartMainLoop();
        }

        private void TrayIcon()
        {
            var menu = new System.Windows.Forms.ContextMenuStrip();
            menu.Items.Add("Open", null, new EventHandler(OnOpenClick));
            menu.Items.Add("Change All", null, new EventHandler(OnChangeAllClick));
            menu.Items.Add("Black mode", null, new EventHandler(OnBlackModeClick));
            menu.Items.Add("New images", null, new EventHandler(OnNewImagesClick));
            menu.Items.Add("Open images folder", null, new EventHandler(OnOpenImagesClick));
            menu.Items.Add("Close", null, new EventHandler(OnCloseClick));
            trayIcon = new System.Windows.Forms.NotifyIcon()
            {
                Icon = WallpaperChanger.Resources.AppIcon,
                ContextMenuStrip = menu,
                Visible = true
            };
            trayIcon.DoubleClick += OnOpenClick;
        }

        private void OnBlackModeClick(object sender, EventArgs eventArgs)
        {
            blackMode = true;
            changer.ChangeAllWallpaper(true);
            changer.doChanges();
        }

        private void OnChangeAllClick(object sender, EventArgs eventArgs)
        {
            blackMode = false;
            changer.ChangeAllWallpaper();
        }

        private void OnOpenClick(object sender, EventArgs eventArgs)
        {
            changer.OpenGUI();
        }

        private void OnNewImagesClick(object sender, EventArgs eventArgs)
        {
            imageDler.OpenGUI();
        }

        private void OnOpenImagesClick(object sender, EventArgs eventArgs)
        {
            Process.Start("explorer.exe", imageContainer.imageFolder);
        }

        private void OnCloseClick(object sender, EventArgs eventArgs)
        {
            running = false;
            worker.Join();
            persister.AddForSave(changer);
            persister.AddForSave(imageDler);
            persister.Save();
            Shutdown();
        }

        private void StartMainLoop()
        {
            worker = new Thread(MainLoop);
            worker.Start();
        }

        private void MainLoop()
        { 
            running = true;
            while(running)
            {
                if(!blackMode) changer.doChanges();
                Thread.Sleep(1000);
            }
        }
    }
}
