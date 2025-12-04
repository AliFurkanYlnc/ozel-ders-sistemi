import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import StudentHomeScreen from '../screens/Student/StudentHomeScreen';

export type StudentTabsParamList = {
  StudentHome: undefined;
};

const Tab = createBottomTabNavigator<StudentTabsParamList>();

const StudentTabs = () => (
  <Tab.Navigator>
    <Tab.Screen name="StudentHome" component={StudentHomeScreen} options={{ title: 'Ana Sayfa' }} />
  </Tab.Navigator>
);

export default StudentTabs;
