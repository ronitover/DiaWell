import 'dart:convert';
import 'package:http/http.dart' as http;

class DiaWellApiClient {
  static const String baseUrl = 'http://localhost:8000'; // Change for production
  
  // Health check
  static Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/'));
      return json.decode(response.body);
    } catch (e) {
      throw Exception('Failed to connect to DiaWell API: $e');
    }
  }
  
  // Submit risk assessment
  static Future<Map<String, dynamic>> submitRiskAssessment({
    required String name,
    required int age,
    required String gender,
    required double height,
    required double weight,
    required int bpSys,
    required int bpDia,
    required bool historyHighGlucose,
    required double physicalActivityHoursPerWeek,
    required String familyHistoryDiabetes,
    required String smokingStatus,
    required String alcoholStatus,
    String lang = 'en',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/risk/submit'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'name': name,
          'age': age,
          'gender': gender,
          'height': height,
          'weight': weight,
          'bp_sys': bpSys,
          'bp_dia': bpDia,
          'history_high_glucose': historyHighGlucose,
          'physical_activity_hours_per_week': physicalActivityHoursPerWeek,
          'family_history_diabetes': familyHistoryDiabetes,
          'smoking_status': smokingStatus,
          'alcohol_status': alcoholStatus,
          'lang': lang,
        }),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to submit risk assessment: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to submit risk assessment: $e');
    }
  }
  
  // Generate recommendations
  static Future<Map<String, dynamic>> generateRecommendations({
    required String riskLevel,
    required int riskScore,
    required List<String> flags,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/recommendations/generate'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'risk_level': riskLevel,
          'risk_score': riskScore,
          'flags': flags,
        }),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to generate recommendations: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to generate recommendations: $e');
    }
  }
}

// Example usage in Flutter widget
/*
class RiskAssessmentScreen extends StatefulWidget {
  @override
  _RiskAssessmentScreenState createState() => _RiskAssessmentScreenState();
}

class _RiskAssessmentScreenState extends State<RiskAssessmentScreen> {
  bool _isLoading = false;
  Map<String, dynamic>? _result;
  
  Future<void> _submitAssessment() async {
    setState(() => _isLoading = true);
    
    try {
      final result = await DiaWellApiClient.submitRiskAssessment(
        name: 'John Doe',
        age: 45,
        gender: 'male',
        height: 175.0,
        weight: 80.0,
        bpSys: 140,
        bpDia: 90,
        historyHighGlucose: false,
        physicalActivityHoursPerWeek: 3.0,
        familyHistoryDiabetes: 'none',
        smokingStatus: 'never',
        alcoholStatus: 'moderate',
      );
      
      setState(() {
        _result = result;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('DiaWell Risk Assessment')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: _isLoading ? null : _submitAssessment,
              child: _isLoading 
                ? CircularProgressIndicator() 
                : Text('Submit Assessment'),
            ),
            if (_result != null) ...[
              SizedBox(height: 20),
              Text('Risk Score: ${_result!['risk_score']}'),
              Text('Risk Level: ${_result!['risk_level']}'),
              Text('Flags: ${_result!['flags'].join(', ')}'),
            ],
          ],
        ),
      ),
    );
  }
}
*/
