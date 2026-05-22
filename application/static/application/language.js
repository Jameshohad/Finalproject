document.addEventListener("DOMContentLoaded", function () {
  const translateBtn = document.getElementById("translate-btn");

  if (!translateBtn) {
    console.error("translate-btn 没找到");
    return;
  }

  translateBtn.addEventListener("click", function () {
    console.log("翻译按钮被点击了");
  });
});
// 翻译对象 - 包含所有多语言翻译内容
const translations = {
  "zh-CN": {
    // 导航栏
    "nav.home": "主页",
    "nav.courses": "课程",
    "nav.quiz": "测验",
    "nav.about": "关于",
    "nav.signup": "注册",
    "nav.translate": "English",

    // 主页
    "home.banner": "轻松学中文 — 专为所有对中文感兴趣的学习者设计。",
    "home.card1": "中文是世界上使用最广泛的语言之一。",
    "home.card2": "学习中文可以帮助您更好地了解中国文化。",
    "home.card3": "本课程专为所有对中文感兴趣的学习者设计。",
    "home.features": "平台特色",
    "home.feature1": "📊 学习进度跟踪",
    "home.feature2": "🎧 AI发音练习",
    "home.feature3": "📝 每周测验挑战",
    "home.progressTitle": "学习进度追踪",
    "home.lessons": "已学课程",
    "home.quizzes": "完成测验",
    "home.studyTime": "学习时间(小时)",
    "home.overallProgress": "总体进度",
    "home.recentActivity": "最近活动",
    "home.noActivity": "暂无活动记录，开始学习吧！",
    "home.viewProfile": "查看完整个人资料",
    "home.activity1": "完成了HSK1第3课",
    "home.activity2": "通过了日常会话测验",
    "home.activity3": "学习了旅游中文词汇",
    "home.loginPrompt": "登录以继续学习",
    "home.loginPromptDesc": "注册或登录您的账户，开始跟踪您的学习进度",
    "home.loginButton": "立即登录",
    "home.signupButton": "注册账户",
    "home.logout": "🚪 登出",
    "home.userwelcome": "欢迎👋",

    // 课程页面
    "courses.title": "开始您的个性化中文学习之旅",
    "course1.title": "HSK 1 初级课程",
    "course1.item1": "📚 150个基础词汇",
    "course1.item2": "📝 基本语法结构",
    "course1.item3": "🗣️ 日常对话练习",
    "course1.item4": "🎧 标准发音训练",
    "course1.item5": "📊 进度跟踪系统",
    "course1.button": "开始学习",
    "course2.title": "日常会话课程",
    "course2.item1": "👋 问候与介绍",
    "course2.item2": "🍽️ 餐厅点餐用语",
    "course2.item3": "🛒 购物对话练习",
    "course2.item4": "🏨 酒店住宿交流",
    "course2.item5": "🚕 交通出行对话",
    "course2.button": "立即体验",
    "course3.title": "旅游中文课程",
    "course3.item1": "✈️ 机场常用表达",
    "course3.item2": "🏨 酒店入住退房",
    "course3.item3": "🗺️ 问路与方向",
    "course3.item4": "🍜 美食文化介绍",
    "course3.item5": "🚨 紧急情况用语",
    "course3.button": "了解更多",

    // 测验页面
    "quiz.title": "中文水平测验",
    "quiz.progress": "问题 1 / 5",
    "quiz.question1": "问题将在这里显示",
    "quiz.next": "下一题 →",

    // 关于页面
    "about.title": "关于 Learn Chinese 平台",
    "about.intro":
      "Learn Chinese 是一个创新的在线中文学习平台，致力于帮助全球学习者掌握基础中文交流技能。我们相信语言学习应该是愉快、实用且有效的体验。",
    "about.mission.title": "🎯 我们的使命",
    "about.features.title": "✨ 平台特色",
    "about.team.title": "👥 我们的团队",
    "about.contact.title": "📧 联系我们",
    "about.teach":
      "我们的平台采用先进的教学方法，结合现代科技，为学习者提供个性化的学习路径。无论您是零基础的初学者，还是希望提升商务中文能力，我们都有适合您的课程",
    "about.ability":
      "让中文学习变得简单、实用且有趣。我们专注于日常生活对话和真实场景应用，帮助学习者在最短时间内获得实际交流能力。",
    "about.feature1": "个性化学习路径 - 根据您的水平和目标定制学习计划",
    "about.feature2": "AI发音评估 - 实时反馈发音准确性",
    "about.feature3": "互动式练习 - 游戏化学习体验",
    "about.feature4": "文化融入 - 学习语言同时了解中国文化",
    "about.feature5": "进度追踪 - 可视化学习成果和进步",
    "about.team1":
      "我们由经验丰富的语言教育专家、技术开发者和用户体验设计师组成。团队成员来自中国、美国、欧洲等地，拥有多元文化背景和国际化的教学理念。",
    "about.background": "💻 项目背景",
    "about.background1":
      "这个学习网站最初是作为一个学生项目创建的，旨在结合前端网页开发技术和语言学习科技。我们希望通过这个平台展示如何利用现代技术提升语言学习效率。",
    "about.contact":
      "如果您有任何问题或建议，欢迎通过以下方式联系我们：📧 邮箱: contact@learnchinese.com | 📱 电话: +7 911 000 0000 | 🏢 地址: 俄罗斯叶卡捷琳堡市和平街",
    "about.ready": "准备好开始您的中文学习之旅了吗？",
    "about.ready1": "立即注册免费账户",

    // 注册页面
    "signup.title": "创建您的免费账户",
    "signup.subtitle": "加入全球中文学习者社区，开始您的语言学习之旅",
    "signup.username": "👤 用户名",
    "signup.username1": "英文字母、数字或中文，不能包含特殊字符",
    "signup.inputusername": "请输入用户名",
    "signup.mail": "📧 邮箱地址",
    "signup.mail1": "我们将通过此邮箱发送验证邮件",
    "signup.inputmail": "请输入有效邮箱地址",
    "signup.password": "🔒 密码",
    "signup.inputpassword": "请输入密码 (至少8位)",
    "signup.passwordstrong": "密码强度: 弱",
    "signup.confirmPassword": "🔑 确认密码",
    "signup.passwordagain": "请再次输入密码",
    "signup.passwordmakesure": "请确保两次输入的密码一致",
    "signup.puropose": "🎯 您的学习目标是什么？",
    "signup.puropose1": "零基础入门",
    "signup.puropose2": "日常会话",
    "signup.puropose3": "商务中文",
    "signup.puropose4": "旅游交流",
    "signup.creat": "🚀 创建账户",
    "signup.haveaccount": "已有账户？",
    "signup.logininm": "立即登录",
    "signup.logindifferent": "或使用以下方式注册",
    "signup.wechat": "微信",

    // 登录页面
    "login.title": "登录您的账户",
    "login.subtitle": "欢迎回来！请登录您的账户继续学习中文",
    "login.email": "📧 邮箱地址",
    "login.emailPlaceholder": "请输入您的邮箱地址",
    "login.emailHint": "请输入注册时使用的邮箱地址",
    "login.password": "🔒 密码",
    "login.passwordPlaceholder": "请输入您的密码",
    "login.passwordHint": "请输入您的账户密码",
    "login.remember": "记住我",
    "login.forgot": "忘记密码？",
    "login.submit": "🚀 登录",
    "login.noAccount": "还没有账户？",
    "login.signupNow": "立即注册",
    "login.orLogin": "或使用以下方式登录",
    "login.success": "登录成功！",
    "login.successMessage": "欢迎回到 Learn Chinese！正在重定向到首页...",
    "login.redirect": "将在 3 秒后重定向",

    // 页脚
    "footer.copyright": "© 2025 Learn Chinese. 保留所有权利。",
    "footer.slogan": "让世界听见中文的声音！",
  },
  en: {
    // Navigation
    "nav.home": "Home",
    "nav.courses": "Courses",
    "nav.quiz": "Quiz",
    "nav.about": "About",
    "nav.signup": "Sign Up",
    "nav.translate": "中文",

    // Home
    "home.banner":
      "Learn Chinese Easily — Designed for all Chinese language enthusiasts.",
    "home.card1":
      "Chinese is one of the most widely spoken languages in the world.",
    "home.card2":
      "Learning Chinese helps you better understand Chinese culture.",
    "home.card3":
      "This course is designed for all learners interested in Chinese.",
    "home.features": "Platform Features",
    "home.feature1": "📊 Learning Progress Tracking",
    "home.feature2": "🎧 AI Pronunciation Practice",
    "home.feature3": "📝 Weekly Quiz Challenges",
    "home.progressTitle": "Learning Progress",
    "home.lessons": "Lessons Completed",
    "home.quizzes": "Quizzes Passed",
    "home.studyTime": "Study Time (hours)",
    "home.overallProgress": "Overall Progress",
    "home.recentActivity": "Recent Activity",
    "home.noActivity": "No activity yet. Start learning!",
    "home.viewProfile": "View Full Profile",
    "home.activity1": "Completed HSK1 Lesson 3",
    "home.activity2": "Passed Daily Conversation Quiz",
    "home.activity3": "Learned Travel Chinese Vocabulary",
    "home.loginPrompt": "Login to Continue Learning",
    "home.loginPromptDesc":
      "Register or login to your account to start tracking your learning progress",
    "home.loginButton": "Login Now",
    "home.signupButton": "Create Account",
    "home.logout": "🚪 Logout",
    "home.userwelcome": "Welcome👋",

    // Courses
    "courses.title": "Start Your Personalized Chinese Learning Journey",
    "course1.title": "HSK 1 Beginner Course",
    "course1.item1": "📚 150 Basic Vocabulary",
    "course1.item2": "📝 Basic Grammar Structures",
    "course1.item3": "🗣️ Daily Conversation Practice",
    "course1.item4": "🎧 Standard Pronunciation Training",
    "course1.item5": "📊 Progress Tracking System",
    "course1.button": "Start Learning",
    "course2.title": "Daily Conversation Course",
    "course2.item1": "👋 Greetings and Introductions",
    "course2.item2": "🍽️ Restaurant Ordering",
    "course2.item3": "🛒 Shopping Dialogues",
    "course2.item4": "🏨 Hotel Accommodation",
    "course2.item5": "🚕 Transportation Communication",
    "course2.button": "Try Now",
    "course3.title": "Travel Chinese Course",
    "course3.item1": "✈️ Airport Expressions",
    "course3.item2": "🏨 Hotel Check-in/out",
    "course3.item3": "🗺️ Asking Directions",
    "course3.item4": "🍜 Food Culture Introduction",
    "course3.item5": "🚨 Emergency Situations",
    "course3.button": "Learn More",

    // Quiz
    "quiz.title": "Chinese Proficiency Test",
    "quiz.progress": "Question 1 / 5",
    "quiz.question1": "Question will be displayed here",
    "quiz.next": "Next Question →",

    // About
    "about.title": "About Learn Chinese Platform",
    "about.intro":
      "Learn Chinese is an innovative online Chinese learning platform dedicated to helping global learners master basic Chinese communication skills. We believe language learning should be enjoyable, practical, and effective.",
    "about.mission.title": "🎯 Our Mission",
    "about.features.title": "✨ Platform Features",
    "about.team.title": "👥 Our Team",
    "about.contact.title": "📧 Contact Us",
    "about.teach":
      "Our platform employs advanced teaching methods combined with modern technology to provide learners with personalized learning paths. Whether you are a complete beginner or wish to improve your business Chinese skills, we have courses suitable for you.",
    "about.ability":
      "Making Chinese learning simple, practical, and fun. We focus on daily life conversations and real-world scenario applications, helping learners acquire practical communication skills in the shortest time possible.",
    "about.feature1":
      "Personalized Learning Path - Customized learning plans based on your level and goals",
    "about.feature2":
      "AI Pronunciation Assessment - Real-time feedback on pronunciation accuracy",
    "about.feature3": "Interactive Exercises - Gamified learning experience",
    "about.feature4":
      "Cultural Integration - Learn the language while understanding Chinese culture",
    "about.feature5":
      "Progress Tracking - Visualize learning outcomes and improvements",
    "about.team1":
      "We are composed of experienced language education experts, technology developers, and user experience designers. Team members come from China, the United States, Europe, and other regions, possessing diverse cultural backgrounds and an international teaching philosophy.",
    "about.background": "💻 Project Background",
    "about.background1":
      "This learning website was initially created as a student project, aiming to combine front-end web development technology with language learning technology. We hope to demonstrate through this platform how modern technology can enhance language learning efficiency.",
    "about.contact":
      "If you have any questions or suggestions, please feel free to contact us via the following methods: Email: contact@learnchinese.com | Phone: +7 911 000 0000 | Address: Mira Street, Yekaterinburg, Russia",
    "about.ready": "Ready to start your Chinese learning journey?",
    "about.ready1": "Sign Up for a Free Account Now",

    // Signup
    "signup.title": "Create Your Free Account",
    "signup.subtitle":
      "Join the global Chinese learners community and start your language learning journey",
    "signup.username": "👤 Username",
    "signup.username1":
      "English letters, numbers, or Chinese characters are acceptable, but special characters are not allowed",
    "signup.inputusername": "Please enter your username",
    "signup.mail": "📧 Email Address",
    "signup.mail1": "We will send a verification email to this address",
    "signup.inputmail": "Please enter a valid email address",
    "signup.password": "🔒 Password",
    "signup.inputpassword":
      "Please enter your password (at least 8 characters)",
    "signup.passwordstrong": "Password strength: Weak",
    "signup.confirmPassword": "🔑 Confirm Password",
    "signup.passwordagain": "Please enter your password again",
    "signup.passwordmakesure":
      "Please ensure that the passwords you enter match",
    "signup.puropose": "🎯 What are your learning goals?",
    "signup.puropose1": "Beginner",
    "signup.puropose2": "Daily Conversation",
    "signup.puropose3": "Business Chinese",
    "signup.puropose4": "Tourism Exchange",
    "signup.creat": "🚀 Create Account",
    "signup.haveaccount": "Already have an account?",
    "signup.logininm": "Log in now",
    "signup.logindifferent": "Or register using the following methods",
    "signup.wechat": "WeChat",

    // Login
    "login.title": "Login to Your Account",
    "login.subtitle": "Welcome back! Please login to continue learning Chinese",
    "login.email": "📧 Email Address",
    "login.emailPlaceholder": "Enter your email address",
    "login.emailHint": "Please enter the email used during registration",
    "login.password": "🔒 Password",
    "login.passwordPlaceholder": "Enter your password",
    "login.passwordHint": "Please enter your account password",
    "login.remember": "Remember me",
    "login.forgot": "Forgot password?",
    "login.submit": "🚀 Login",
    "login.noAccount": "Don't have an account?",
    "login.signupNow": "Sign up now",
    "login.orLogin": "Or login using",
    "login.success": "Login successful!",
    "login.successMessage":
      "Welcome back to Learn Chinese! Redirecting to homepage...",
    "login.redirect": "Redirecting in 3 seconds",

    // Footer
    "footer.copyright": "© 2025 Learn Chinese. All rights reserved.",
    "footer.slogan": "Let the world hear the voice of Chinese!",
  },
};

// 当前语言设置
let currentLanguage = "zh-CN";

// 初始化翻译功能
function initTranslation() {
  // 从本地存储获取语言设置
  const savedLang = localStorage.getItem("preferredLanguage");
  if (savedLang) {
    currentLanguage = savedLang;
  }

  // 应用翻译
  applyTranslations(currentLanguage);

  // 创建翻译按钮事件监听
  const translateBtn = document.getElementById("translate-btn");
  if (translateBtn) {
    translateBtn.addEventListener("click", function (e) {
      e.preventDefault();
      toggleLanguage();
    });
  }

  // 更新按钮文本
  updateTranslateButton();
}

// 切换语言
function toggleLanguage() {
  currentLanguage = currentLanguage === "zh-CN" ? "en" : "zh-CN";

  // 保存到本地存储
  localStorage.setItem("preferredLanguage", currentLanguage);

  // 应用翻译
  applyTranslations(currentLanguage);

  // 更新按钮文本
  updateTranslateButton();

  // 添加切换动画
  document.body.style.transition = "opacity 0.3s ease";
  document.body.style.opacity = "0.8";
  setTimeout(() => {
    document.body.style.opacity = "1";
  }, 150);
}

// 应用翻译到页面元素
function applyTranslations(lang) {
  const elements = document.querySelectorAll("[data-translate]");

  elements.forEach((element) => {
    const key = element.getAttribute("data-translate");

    // 检查翻译是否存在
    if (translations[lang] && translations[lang][key]) {
      const translationText = translations[lang][key];

      // 根据元素类型应用翻译
      if (element.tagName === "INPUT" || element.tagName === "TEXTAREA") {
        // 对于输入框，使用placeholder
        element.placeholder = translationText;
      } else if (element.tagName === "IMG") {
        // 对于图片，使用alt属性
        element.alt = translationText;
      } else {
        // 对于其他元素，使用innerHTML（支持HTML标签）
        element.textContent = translationText;
      }
    } else {
      console.warn(`翻译不存在: ${lang}.${key}`);
    }
  });

  // 更新页面语言属性
  document.documentElement.lang = lang;
  console.log(`语言已切换为: ${lang}`);
}

// 更新翻译按钮文本
function updateTranslateButton() {
  const translateBtn = document.getElementById("translate-btn");
  if (translateBtn) {
    // 按钮本身需要有 data-translate 属性
    if (!translateBtn.hasAttribute("data-translate")) {
      // 如果没有，直接设置文本
      translateBtn.textContent =
        currentLanguage === "zh-CN" ? "English" : "中文";
    }
  }
}

// 页面加载完成后初始化翻译
document.addEventListener("DOMContentLoaded", function () {
  console.log("开始初始化翻译系统...");
  initTranslation();
});

// 防止脚本加载失败时的错误
window.addEventListener("error", function (event) {
  console.error("脚本错误:", event.error);
});
