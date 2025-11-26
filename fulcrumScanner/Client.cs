using fingerprintScanner;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace fulcrumScanner
{

    internal class Client
    {
        private Futonic futonic;
        public Client(Futonic futonic)
        {
            this.futonic = futonic;
        }


        public async Task<string> SendToPython()
        {
            byte[] bmp = futonic.getBMP();
            if (bmp == null)
                return "Brak obrazu z sensora";

            using (var client = new HttpClient())
            using (var content = new MultipartFormDataContent())
            {
                var byteContent = new ByteArrayContent(bmp);
                byteContent.Headers.ContentType = MediaTypeHeaderValue.Parse("image/bmp");
                content.Add(byteContent, "file", "fingerprin.bmp");

                var response = await client.PostAsync("http://127.0.0.1:8000/predict", content);

                if (!response.IsSuccessStatusCode)
                {
                    MessageBox.Show($"Błąd połączenia: {response.StatusCode}");
                    return null;
                }

                var result = response.Content.ReadAsStringAsync();
                string text = await result;

                MessageBox.Show(text);
                return await result;
            }
        }
    }
}
