// mobile/App.js

import React, { useState, useEffect, useRef } from 'react';
import {
  ActivityIndicator,
  Alert,
  Button,
  FlatList,
  KeyboardAvoidingView,
  SafeAreaView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import io from 'socket.io-client';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const SERVER_URL = 'http://<YOUR_BACKEND_HOST>:5000'; // e.g., 'http://10.0.2.2:5000' on Android emulator

// --- Authentication Screen ---
function AuthScreen({ navigation }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername]   = useState('');
  const [email, setEmail]         = useState('');
  const [password, setPassword]   = useState('');
  const [loading, setLoading]     = useState(false);

  const handleRegister = async () => {
    if (!username || !email || !password) {
      Alert.alert('All fields are required');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${SERVER_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      });
      const data = await res.json();
      if (res.ok) {
        Alert.alert('Registered successfully. Please login.');
        setIsRegister(false);
      } else {
        Alert.alert(data.error || 'Registration failed');
      }
    } catch (err) {
      console.error(err);
      Alert.alert('Server error');
    }
    setLoading(false);
  };

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('All fields are required');
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${SERVER_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        await AsyncStorage.setItem('token', data.token);
        await AsyncStorage.setItem('username', data.username);
        navigation.replace('Chat');
      } else {
        Alert.alert(data.error || 'Login failed');
      }
    } catch (err) {
      console.error(err);
      Alert.alert('Server error');
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#1abc9c" />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.authContainer}>
      <Text style={styles.title}>TrojanChat</Text>

      {isRegister && (
        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
        />
      )}
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      {isRegister ? (
        <Button title="Register" color="#1abc9c" onPress={handleRegister} />
      ) : (
        <Button title="Login" color="#1abc9c" onPress={handleLogin} />
      )}

      <TouchableOpacity
        style={{ marginTop: 16 }}
        onPress={() => setIsRegister(!isRegister)}
      >
        <Text style={styles.link}>
          {isRegister
            ? 'Already have an account? Login'
            : "Don't have an account? Register"}
        </Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

// --- Chat Screen ---
function ChatScreen({ navigation }) {
  const [messages, setMessages] = useState([]);
  const [msgText, setMsgText]   = useState('');
  const [currentRoom, setCurrentRoom] = useState('General');
  const [username, setUsername] = useState('');
  const [socketConnected, setSocketConnected] = useState(false);
  const socketRef = useRef(null);
  const flatListRef = useRef();

  useEffect(() => {
    // Load stored username
    AsyncStorage.getItem('username').then((u) => {
      if (u) setUsername(u);
    });

    const tokenPromise = AsyncStorage.getItem('token');
    tokenPromise.then((token) => {
      if (!token) {
        navigation.replace('Auth');
        return;
      }
      // Connect to Socket.io with JWT
      const socket = io(SERVER_URL, { auth: { token } });
      socketRef.current = socket;

      socket.on('connect', () => {
        setSocketConnected(true);
        joinRoom(currentRoom);
      });
      socket.on('disconnect', () => {
        setSocketConnected(false);
      });

      // Receive chat history
      socket.on('roomHistory', (history) => {
        setMessages(history);
        setTimeout(() => {
          flatListRef.current?.scrollToEnd({ animated: true });
        }, 100);
      });

      // Receive a new message
      socket.on('message', (msgObj) => {
        setMessages((prev) => [...prev, msgObj]);
        setTimeout(() => {
          flatListRef.current?.scrollToEnd({ animated: true });
        }, 100);
      });
    });

    return () => {
      socketRef.current?.disconnect();
    };
  }, []);

  const joinRoom = (room) => {
    setMessages([]); // clear
    socketRef.current?.emit('joinRoom', room);
  };

  const sendMessage = () => {
    const text = msgText.trim();
    if (!text) return;
    const msgObj = { room: currentRoom, text, username };
    socketRef.current.emit('chatMessage', msgObj);
    setMsgText('');
  };

  const handleLogout = async () => {
    await AsyncStorage.removeItem('token');
    await AsyncStorage.removeItem('username');
    socketRef.current.disconnect();
    navigation.replace('Auth');
  };

  const renderItem = ({ item }) => (
    <View style={styles.messageItem}>
      <Text style={styles.messageUser}>{item.username}:</Text>
      <Text style={styles.messageText}>{item.text}</Text>
      <Text style={styles.messageTime}>
        {new Date(item.timestamp).toLocaleTimeString()}
      </Text>
    </View>
  );

  return (
    <SafeAreaView style={styles.chatContainer}>
      <View style={styles.chatHeader}>
        <Text style={styles.chatTitle}>Room: {currentRoom}</Text>
        <Button title="Logout" color="#e74c3c" onPress={handleLogout} />
      </View>

      <View style={styles.roomsBar}>
        {['General', 'USCFootball', 'Sports'].map((room) => (
          <TouchableOpacity
            key={room}
            style={[
              styles.roomButton,
              currentRoom === room && styles.roomButtonActive
            ]}
            onPress={() => {
              setCurrentRoom(room);
              joinRoom(room);
            }}
          >
            <Text
              style={[
                styles.roomButtonText,
                currentRoom === room && styles.roomButtonTextActive
              ]}
            >
              {room}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(item, index) => index.toString()}
        renderItem={renderItem}
        style={styles.messagesList}
      />

      <KeyboardAvoidingView behavior="padding" style={styles.inputBar}>
        <TextInput
          style={styles.inputField}
          placeholder="Type a message"
          value={msgText}
          onChangeText={setMsgText}
        />
        <Button title="Send" color="#1abc9c" onPress={sendMessage} />
      </KeyboardAvoidingView>

      {!socketConnected && (
        <View style={styles.centeredOverlay}>
          <ActivityIndicator size="large" color="#1abc9c" />
          <Text style={{ color: '#555', marginTop: 8 }}>Connecting...</Text>
        </View>
      )}
    </SafeAreaView>
  );
}

// --- Navigation Setup ---
const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Auth" screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Auth" component={AuthScreen} />
        <Stack.Screen name="Chat" component={ChatScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// --- Styles ---
const styles = StyleSheet.create({
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  authContainer: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
    backgroundColor: '#ecf0f1',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1abc9c',
    textAlign: 'center',
    marginBottom: 24,
  },
  input: {
    borderWidth: 1,
    borderColor: '#bdc3c7',
    borderRadius: 4,
    padding: 12,
    marginVertical: 8,
    backgroundColor: '#fff',
  },
  link: {
    color: '#3498db',
    textAlign: 'center',
  },
  chatContainer: {
    flex: 1,
    backgroundColor: '#ecf0f1',
  },
  chatHeader: {
    backgroundColor: '#1abc9c',
    paddingVertical: 12,
    paddingHorizontal: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  chatTitle: {
    fontSize: 18,
    color: '#fff',
    fontWeight: 'bold',
  },
  roomsBar: {
    flexDirection: 'row',
    backgroundColor: '#2c3e50',
  },
  roomButton: {
    flex: 1,
    paddingVertical: 10,
    alignItems: 'center',
  },
  roomButtonActive: {
    backgroundColor: '#34495e',
  },
  roomButtonText: {
    color: '#ecf0f1',
    fontWeight: 'bold',
  },
  roomButtonTextActive: {
    color: '#1abc9c',
  },
  messagesList: {
    flex: 1,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  messageItem: {
    marginBottom: 12,
    backgroundColor: '#fff',
    padding: 8,
    borderRadius: 4,
    elevation: 2,
  },
  messageUser: {
    fontWeight: 'bold',
    marginBottom: 4,
    color: '#2c3e50',
  },
  messageText: {
    fontSize: 16,
    marginBottom: 4,
    color: '#333',
  },
  messageTime: {
    fontSize: 12,
    color: '#7f8c8d',
    textAlign: 'right',
  },
  inputBar: {
    flexDirection: 'row',
    padding: 8,
    borderTopWidth: 1,
    borderColor: '#bdc3c7',
    backgroundColor: '#fff',
  },
  inputField: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#bdc3c7',
    borderRadius: 4,
    paddingHorizontal: 12,
    marginRight: 8,
    backgroundColor: '#fff',
  },
  centeredOverlay: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.2)',
  },
});
