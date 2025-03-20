import 'package:flutter/material.dart';
import 'package:frontend/questionnaire_screen.dart';
import 'camera_screen.dart';

class SeverityLevelScreen extends StatelessWidget {
  final String selectedType;

  const SeverityLevelScreen({Key? key, required this.selectedType}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final severityLevels = [
      {'title': 'Mild', 'description': 'Slight difficulty to identify certain colors'},
      {'title': 'Moderate', 'description': 'Notable difficulty with color discrimination'},
      {'title': 'Severe', 'description': 'Significant difficulty identifying most colors'},
    ];

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Select Your Severity Level for $selectedType',
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
                fontFamily: 'Serif',
              ),
            ),
            const SizedBox(height: 20),
            ...severityLevels.map((level) {
              return _buildSeverityCard(
                context,
                level['title']!,
                level['description']!,
              );
            }).toList(),
            const SizedBox(height: 30),
            Center(
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => QuestionnaireScreen(
                          colorBlindnessType: selectedType,
                          selectedSeverity: 'Unknown', // Default or dynamically handled severity
                        ),
                      ),
                    );
                  },
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
    );
  }

  Widget _buildSeverityCard(BuildContext context, String title, String description) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => CameraScreen(
              selectedType: selectedType,
              selectedSeverity: title,  // Pass severity directly to CameraScreen
            ),
          ),
        );
      },
      child: Padding(
        padding: const EdgeInsets.only(bottom: 10.0),
        child: Card(
          elevation: 0,
          color: const Color(0xFFF5F5F5),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          child: ListTile(
            title: Text(
              title,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                fontFamily: 'Serif',
              ),
            ),
            subtitle: Text(
              description,
              style: const TextStyle(
                color: Colors.grey,
                fontFamily: 'Serif',
              ),
            ),
            trailing: const Icon(Icons.arrow_forward, color: Colors.grey),
          ),
        ),
      ),
    );
  }
}
