using fingerprintScanner;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;
namespace fulcrumScanner
{

    internal class Client
    {
        private Futonic futonic;
        public Client(Futonic futonic)
        {
            this.futonic = futonic;
        }



        public async Task<(string gender, string confidence, double rawScore)> SendToPython()
        {
            byte[] bmp = futonic.getBMP();
            if (bmp == null)
                return (null, null, 0);

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
                    return (null, null, 0);
                }

                string json = await response.Content.ReadAsStringAsync();

                using (JsonDocument doc = JsonDocument.Parse(json))
                {
                    JsonElement root = doc.RootElement;

                    string gender = root.TryGetProperty("gender", out JsonElement genderElement) ? genderElement.GetString() : null;
                    string confidence = root.TryGetProperty("confidence", out JsonElement confidenceElement) ? confidenceElement.GetString() : null;
                    double rawScore = root.TryGetProperty("raw_score", out JsonElement rawElement) ? rawElement.GetDouble() : 0;

                    // Opcjonalnie: wyświetlenie wszystkich pól
                    MessageBox.Show($"Gender: {gender}\nConfidence: {confidence}\nRaw score: {rawScore}");

                    return (gender, confidence, rawScore);
                }
            }
        }
    }

 }
