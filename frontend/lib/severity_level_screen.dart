import 'package:flutter/material.dart';
import 'questionnaire_screen.dart';


class SeverityLevelScreen extends StatelessWidget {
  const SeverityLevelScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black),
        title: const Padding(
          padding: EdgeInsets.only(top: 16.0),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Select Your Severity Level',
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                fontFamily: 'Serif',
              ),
            ),
            const SizedBox(height: 20),
            _buildSeverityCard('Mild', 'Slight difficulty to identify certain colors'),
            _buildSeverityCard('Moderate', 'Notable difficulty with color discrimination'),
            _buildSeverityCard('Severe', 'Significant difficulty identifying most colors'),
            const SizedBox(height: 30),
            Center(
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.grey[300],
                    padding: const EdgeInsets.symmetric(vertical: 15),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: const Text(
                    'Need Help?',
                    style: TextStyle(
                      fontSize: 16,
                      fontFamily: 'Serif',
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const QuestionnaireScreen()),
          );
        },
        backgroundColor: Colors.white,
        child: const Icon(Icons.arrow_forward, color: Colors.black),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    );
  }

  Widget _buildSeverityCard(String title, String description) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10.0),
      child: Card(
        elevation: 0,
        color: const Color(0xFFF5F5F5),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Serif',
                ),
              ),
              Text(
                description,
                style: const TextStyle(
                  color: Colors.grey,
                  fontFamily: 'Serif',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

