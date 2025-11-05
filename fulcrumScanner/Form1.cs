using fingerprintScanner;

namespace fulcrumScanner
{
    public partial class Form1 : Form
    {
        Futonic futronic = new Futonic();
        bool x2 = false;

        public Form1()
        {
            InitializeComponent();
            predict_label.Visible = false;
            check_sex.Visible = false;

        }



        private void scan_button_Click(object sender, EventArgs e)
        {
            x2 = futronic.Init();

            if (x2 == true)
            {
                var v = futronic.ExportBitMap();

                v.Save("C:\\Users\\akabe\\Desktop\\finger_folder\\taken_fingerprint.bmp", System.Drawing.Imaging.ImageFormat.Bmp);
                fingerpicture.Image = v;
                var b = futronic.IsFinger();
            }
            scan_button.Text = "Powtórz pomiar";
            check_sex.Visible = true;

        }

        private void check_sex_Click(object sender, EventArgs e)
        {
            predict_label.Visible = true;
        }
    }
}
