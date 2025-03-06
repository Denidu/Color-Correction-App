import 'package:flutter/material.dart';
//import 'camera_correction_screen.dart';


class QuestionnaireScreen extends StatelessWidget {
  const QuestionnaireScreen({Key? key}) : super(key: key);

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
            // Progress bar
            Row(
              children: [
                Container(
                  width: 40,
                  height: 4,
                  color: Colors.deepPurple,
                ),
                Expanded(
                  child: Container(
                    height: 4,
                    color: Colors.grey[300],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 15),
            const Text(
              'Question 1 of 10',
              style: TextStyle(
                color: Colors.grey,
                fontFamily: 'Serif',
              ),
            ),
            const SizedBox(height: 15),
            const Text(
              'How often do you have difficulty matching clothes due to colors?',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                fontFamily: 'Serif',
              ),
            ),
            const SizedBox(height: 30),
            _buildAnswerOption('Rarely or never'),
            _buildAnswerOption('Sometimes'),
            _buildAnswerOption('Often'),
            _buildAnswerOption('Almost always'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Navigator.push(
          //   context,
          //   MaterialPageRoute(builder: (context) => const CameraAndCorrectionScreen()),
          // );
        },
        backgroundColor: Colors.white,
        child: const Icon(Icons.arrow_forward, color: Colors.black),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.endFloat,
    );
  }

  Widget _buildAnswerOption(String text) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10.0),
      child: Card(
        elevation: 0,
        color: const Color(0xFFF5F5F5),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
          child: Text(
            text,
            style: const TextStyle(
              fontSize: 16,
              fontFamily: 'Serif',
            ),
          ),
        ),
      ),
    );
  }
}