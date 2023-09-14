﻿using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using WallpaperChanger.Util;

namespace WallpaperChanger.Shared
{
    public class WpcImage
    {
        public enum Type { UNKNOWN, JPG, PNG }

        public class Size
        {
            public int width { get; }
            public int height { get; }
            public Size(int width, int height)
            {
                this.width = width;
                this.height = height;
            }
            override public string ToString()
            {
                return width + "x" + height;
            }
        }

        public static Type getTypeForExtension(string extension)
        {
            extension = extension.ToLower();
            if (extension == "jpg" || extension == "jpeg") return Type.JPG;
            else if (extension == "png") return Type.PNG;
            return Type.UNKNOWN;
        }

        Type type;
        public string name;
        string extension { get; }
        public string? saveFolder { get; private set; }
        byte[]? data { get; set; }
        public Size? size { get; set; }
        public WpcImage()
        {
            type = Type.UNKNOWN;
            name = "";
            extension = "";            
            saveFolder = "";
            data = null;
            size = null;
        }

        public WpcImage(string path) : this()
        {
            var fullName = Path.GetFileName(path);
            var parts = fullName.Split('.');
            name = parts[0];
            extension = parts[1];
            saveFolder = path.Split(fullName)[0];
            var img = Image.FromFile(path);
            data = FileUtil.ReadBytes(path);
            size = new Size(img.Width, img.Height);
            type = getTypeForExtension(extension);
        }

        public WpcImage(Type type, string name, string extension, Size size, byte[] data)
        {
            this.type = type;
            this.name = name;
            this.extension = extension;
            this.data = data;
            this.size = size;
            saveFolder = "";
        }

        public string getFullName()
        {
            return $"{name}.{extension}";
        }

        public void move(string? newFolder)
        {
            if (saveFolder == null || newFolder == null) return;
            var sourcePath = Path.Combine(saveFolder, getFullName());
            var destPath = Path.Combine(newFolder, getFullName());
            try
            {
                File.Move(sourcePath, destPath);
            } 
            catch (IOException ex)
            {
                Debug.WriteLine("Guess already saved");
            }
            
        }

        public void save()
        {
            save(null);
        }

        public void save(string? saveFolder)
        {
            if (saveFolder != null) this.saveFolder = saveFolder;
            if (this.saveFolder == null) return;
            if (data == null) return;
            FileUtil.SaveBytes(getFullPath(), data);
        }

        public string getFullPath()
        {
            if (saveFolder == null) return Path.GetFullPath(getFullName());
            return Path.GetFullPath(Path.Combine(saveFolder, getFullName()));
        }

        public Image? asImage()
        {
            if (data == null) return null;
            return Image.FromStream(new MemoryStream(data));
        }

        public BitmapSource? asBitmapSource()
        {
            if (data == null) return null;
            var bi = new BitmapImage();
            bi.BeginInit();
            bi.StreamSource = new MemoryStream(data);
            bi.EndInit();
            return bi;
        }

        public void Resize(int width, int height)
        {
            var bitmap = (Bitmap)asImage();
            if (bitmap == null) return;
            var newBitmap = new Bitmap(width, height);
            var canvas = Graphics.FromImage(newBitmap);
            var imageAspectRatio = ((float)bitmap.Width / bitmap.Height);
            var neededAspectRatio = ((float)width / height);
            Debug.WriteLine("Image aspect ratio: " + imageAspectRatio);
            Debug.WriteLine("Needed aspect ratio: " + neededAspectRatio);
            var scaleFactor = 0f;
            var topOffset = 0;
            var leftOffset = 0;
            if (neededAspectRatio == imageAspectRatio)
            {
                Debug.WriteLine("Same aspect ratio");
                scaleFactor = (float)bitmap.Width / width;
            }
            else if(neededAspectRatio > imageAspectRatio)
            {
                Debug.WriteLine("Aspect ratio has more height");
                scaleFactor = (float)bitmap.Width / width;
                var newHeight = (int)(bitmap.Height / scaleFactor);
                leftOffset = (height - newHeight) / 2;
            }
            else
            {
                Debug.WriteLine("Aspect ratio has more width");
                scaleFactor = (float)bitmap.Height / height;
                var newWidth = (int)(bitmap.Width / scaleFactor);
                topOffset = (width - newWidth) / 2;
            }
            bitmap.SetResolution(newBitmap.HorizontalResolution * scaleFactor, newBitmap.VerticalResolution * scaleFactor);
            canvas.InterpolationMode = InterpolationMode.HighQualityBicubic;
            canvas.DrawImage(bitmap, new Point(topOffset, leftOffset));
            canvas.Save();
            var imageData = new MemoryStream();
            newBitmap.Save(imageData, ImageFormat.Jpeg);
            size = new Size(width, height);
            data = imageData.ToArray();
        }

        override public string ToString()
        {
            string toString = "name: " + this.name + "\n";
            toString += "extension: " + this.extension + "\n";
            toString += "saveFolder: " + this.saveFolder + "\n";
            toString += "type: " + this.type.ToString() + "\n";
            if (size != null) { toString += "size: " + this.size.ToString() + "\n"; }
            return toString;
        }
    }
}
