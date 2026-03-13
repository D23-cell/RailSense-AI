import { useEffect, useState } from 'react';
import { StyleSheet, Text, View, StatusBar, TouchableOpacity } from 'react-native';

const SERVER_IP = "10.14.58.199";

export default function App() {
  const [liveCount, setLiveCount] = useState(0);
  const [alertMsg, setAlertMsg] = useState("ALL CLEAR");
  const [isHazard, setIsHazard] = useState(false);
  const [ticketless, setTicketless] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://${SERVER_IP}:8080/get_status`);
        const data = await response.json();
        
        setLiveCount(data.count || 0);
        setTicketless(data.ticketless_count || 0);

        // 🚨 MULTI-ALERT LOGIC FOR MOBILE
        let combinedAlert = "";
        let hazardDetected = false;

        if (data.ticketless_count > 0) {
          combinedAlert = `REVENUE LOSS: ${data.ticketless_count} TICKETLESS`;
          hazardDetected = true;
        } else if (data.security_alert !== "NORMAL") {
          combinedAlert = data.security_alert;
          hazardDetected = true;
        } else if (data.op_alert !== "NORMAL") {
          combinedAlert = data.op_alert;
          hazardDetected = true;
        }

        if (hazardDetected) {
          setIsHazard(true);
          setAlertMsg(combinedAlert.toUpperCase());
        } else {
          setIsHazard(false);
          setAlertMsg("ALL CLEAR");
        }
      } catch (error) {
        setAlertMsg("SEARCHING SERVER...");
      }
    };

    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const verifyTicket = () => {
    fetch(`http://${SERVER_IP}:8080/verify_ticket`, { method: 'POST' });
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      <Text style={styles.header}>🚄 RailSense TTE Pad</Text>

      <View style={styles.card}>
        <Text style={styles.label}>Live Coach Occupancy</Text>
        <Text style={styles.count}>{liveCount}</Text>
        {ticketless > 0 && <Text style={{color:'#ef4444', fontWeight:'bold'}}>Detecting {ticketless} Ticketless</Text>}
      </View>

      <View style={[styles.alertCard, isHazard ? styles.danger : styles.safe]}>
        <Text style={styles.alertText}>{isHazard ? `⚠️ ${alertMsg}` : `✅ ${alertMsg}`}</Text>
      </View>

      <TouchableOpacity style={styles.btn} onPress={verifyTicket}>
        <Text style={styles.btnText}>VERIFY PASSENGER</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0f172a', padding: 20, justifyContent: 'center' },
  header: { fontSize: 26, fontWeight: 'bold', color: '#3b82f6', marginBottom: 30, textAlign: 'center' },
  card: { backgroundColor: '#1e293b', padding: 25, borderRadius: 15, alignItems: 'center', marginBottom: 20 },
  label: { color: '#94a3b8', fontSize: 12, textTransform: 'uppercase' },
  count: { color: '#f8fafc', fontSize: 80, fontWeight: 'bold' },
  alertCard: { padding: 20, borderRadius: 12, alignItems: 'center', marginBottom: 20 },
  safe: { backgroundColor: 'rgba(34, 197, 94, 0.15)', borderColor: '#22c55e', borderWidth: 1 },
  danger: { backgroundColor: 'rgba(239, 68, 68, 0.15)', borderColor: '#ef4444', borderWidth: 1 },
  alertText: { fontSize: 16, fontWeight: 'bold', color: '#f8fafc', textAlign: 'center' },
  btn: { backgroundColor: '#3b82f6', padding: 18, borderRadius: 10, alignItems: 'center' },
  btnText: { color: 'white', fontWeight: 'bold', fontSize: 16 }
});