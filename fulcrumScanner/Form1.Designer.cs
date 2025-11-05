namespace fulcrumScanner
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            scan_button = new Button();
            fingerpicture = new PictureBox();
            predict_label = new Label();
            check_sex = new Button();
            ((System.ComponentModel.ISupportInitialize)fingerpicture).BeginInit();
            SuspendLayout();
            // 
            // scan_button
            // 
            scan_button.Font = new Font("Segoe UI", 12F, FontStyle.Bold, GraphicsUnit.Point, 238);
            scan_button.Location = new Point(37, 19);
            scan_button.Name = "scan_button";
            scan_button.Size = new Size(171, 70);
            scan_button.TabIndex = 0;
            scan_button.Text = "Skanuj linie papilarne";
            scan_button.UseVisualStyleBackColor = true;
            scan_button.Click += scan_button_Click;
            // 
            // fingerpicture
            // 
            fingerpicture.Location = new Point(258, 91);
            fingerpicture.Name = "fingerpicture";
            fingerpicture.Size = new Size(269, 322);
            fingerpicture.TabIndex = 1;
            fingerpicture.TabStop = false;
            // 
            // predict_label
            // 
            predict_label.AutoSize = true;
            predict_label.Font = new Font("Segoe UI", 12F, FontStyle.Bold);
            predict_label.Location = new Point(582, 105);
            predict_label.Name = "predict_label";
            predict_label.Size = new Size(93, 21);
            predict_label.TabIndex = 2;
            predict_label.Text = "Predykcja: ";
            // 
            // check_sex
            // 
            check_sex.Font = new Font("Segoe UI", 12F, FontStyle.Bold);
            check_sex.Location = new Point(582, 19);
            check_sex.Name = "check_sex";
            check_sex.Size = new Size(206, 60);
            check_sex.TabIndex = 3;
            check_sex.Text = "Sprawdź płeć";
            check_sex.UseVisualStyleBackColor = true;
            check_sex.Click += check_sex_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(check_sex);
            Controls.Add(predict_label);
            Controls.Add(fingerpicture);
            Controls.Add(scan_button);
            Name = "Form1";
            Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)fingerpicture).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button scan_button;
        private PictureBox fingerpicture;
        private Label predict_label;
        private Button check_sex;
    }
}
