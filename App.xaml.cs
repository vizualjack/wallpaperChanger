﻿using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Diagnostics;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using WallpaperChanger.Change;
using WallpaperChanger.LoadNew;
using WallpaperChanger.Shared;
using WallpaperChanger.Util;

namespace WallpaperChanger
{
    public partial class App : System.Windows.Application
    {
#if DEBUG
        public static Logger.LogLevel LOGLEVEL = Logger.LogLevel.Debug;
#else
        public static Logger.LogLevel LOGLEVEL = Logger.LogLevel.Error;
#endif

        private static Mutex mutex;

        NotifyIcon trayIcon;
        WpcImageContainer imageContainer;
        Changer changer;
        ImageDler? imageDler;
        Persister persister;
        List<Shared.Screen> screens;
        bool running = false;
        bool blackMode = false;
        Thread worker, tiWorker;
        ToolStripItem blackModeItem;

        public App()
        {
            if (AppIsAlreadyRunning())
            {
                MessageBox.Show("An instance of the application is already running.", "WallpaperChanger");
                Shutdown();
                return;
            }
            Logger.logLevel = LOGLEVEL;
            LoadScreens();
            persister = new Persister(WallpaperChanger.Resources.PERSISTER_PATH);
            imageContainer = new WpcImageContainer(WallpaperChanger.Resources.IMAGE_FOLDER);
            changer = new Changer(imageContainer, screens);
            persister.Load(changer);
            var screen = screens[0];
            try
            {
                imageDler = new ImageDler(imageContainer, new WpcImage.Size(screen.width, screen.height));
                persister.Load(imageDler);
            }
            catch { Logger.Info(this, $"No images for this screen size, imageDler disabled. Width: {screen.width} Height: {screen.height}"); }
            InitTrayIcon();
            StartMainLoop();
        }

        private bool AppIsAlreadyRunning()
        {
            bool isNewInstance;
            mutex = new Mutex(true, "askdas--wadawdwwwAAWD-DDDWASDAWLDAWDL-wwsdadaogkedopgk", out isNewInstance);
            return !isNewInstance;
        }

        private void LoadScreens()
        {
            screens = new List<Shared.Screen>();
            foreach (var wScreen in System.Windows.Forms.Screen.AllScreens)
            {
                screens.Add(new Shared.Screen(wScreen.Bounds.Width, wScreen.Bounds.Height));
            }
            Logger.Info(this, $"Loaded {screens.Count} screens");
        }

        private void InitTrayIcon()
        {
            var menu = new System.Windows.Forms.ContextMenuStrip();
            menu.Items.Add("Open", null, new EventHandler(OnOpenClick));
            menu.Items.Add("Change All", null, new EventHandler(OnChangeAllClick));
            blackModeItem = menu.Items.Add(GetBlackModeItemText(), null, new EventHandler(OnBlackModeClick));
            menu.Items.Add("New images", null, new EventHandler(OnNewImagesClick));
            menu.Items.Add("Open images folder", null, new EventHandler(OnOpenImagesClick));
            menu.Items.Add("Close", null, new EventHandler(OnCloseClick));
            trayIcon = new System.Windows.Forms.NotifyIcon()
            {
                Icon = WallpaperChanger.Resources.AppIcon,
                Text = "Wallpaper Changer",
                ContextMenuStrip = menu,
                Visible = true
            };
            trayIcon.DoubleClick += OnOpenClick;
        }

        private string GetBlackModeItemText()
        {
            return $"Black mode ({(blackMode ? "Active" : "Inactive")})";
        }

        private void OnBlackModeClick(object sender, EventArgs eventArgs)
        {
            blackMode = !blackMode;
            blackModeItem.Text = GetBlackModeItemText();
            changer.ChangeAllWallpaper(blackMode);
            changer.doChanges();
        }

        private void OnChangeAllClick(object sender, EventArgs eventArgs)
        {
            changer.ChangeAllWallpaper();
            changer.doChanges();
        }

        private void OnOpenClick(object sender, EventArgs eventArgs)
        {
            changer.OpenGUI();
        }

        private void OnNewImagesClick(object sender, EventArgs eventArgs)
        {
            if (imageDler != null) imageDler.OpenGUI();
            else MessageBox.Show("There are no images for your screen size", "WallpaperChanger");
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
            if(imageDler != null) persister.AddForSave(imageDler);
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
