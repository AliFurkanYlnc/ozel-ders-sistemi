import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import StudentHomeScreen from '../screens/Student/StudentHomeScreen';
import StudentProfileScreen from '../screens/Student/StudentProfileScreen';
import StudentAvailabilityScreen from '../screens/Student/StudentAvailabilityScreen';

const Tab = createBottomTabNavigator();

const StudentTabs = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="StudentHome"
        component={StudentHomeScreen}
        options={{ title: 'Ana Sayfa' }}
      />
      <Tab.Screen
        name="StudentProfile"
        component={StudentProfileScreen}
        options={{ title: 'Profil' }}
      />
      <Tab.Screen
        name="StudentAvailability"
        component={StudentAvailabilityScreen}
        options={{ title: 'Müsaitlik' }}
      />
    </Tab.Navigator>
  );
};

export default StudentTabs;
