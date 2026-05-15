// 测验数据
// 定义一个包含所有问题的数组，每个问题是一个对象
const questions = [
  {
    question: "“你好” in English means?",
    options: ["Goodbye", "Hello", "Thank you"],
    answer: "Hello",
  },
  {
    question: "How do you say 'Thank you' in Chinese?",
    options: ["对不起", "谢谢", "再见"],
    answer: "谢谢",
  },
  {
    question: "What does '再见' mean?",
    options: ["Hello", "Goodbye", "Please"],
    answer: "Goodbye",
  },
  {
    question: "How do you say 'I love you' in Chinese?",
    options: ["我爱你", "你好", "谢谢"],
    answer: "我爱你",
  },
  {
    question: "What does '谢谢' mean?",
    options: ["Sorry", "Thank you", "Goodbye"],
    answer: "Thank you",
  },
];
// ======================= 全局状态变量 ======================= // 记录当前测验进行到哪里
let currentQuestion = 0; // 当前题目索引（从0开始）
let score = 0; // 当前得分（答对+1）
let selectedOption = null; // 当前题是否已选择答案（null=未选）

// DOM元素  // 先把页面元素抓出来，后面反复操作
const questionElement = document.getElementById("question"); // 题目显示区域（ID名称）
const optionsElement = document.getElementById("options");
const feedbackElement = document.getElementById("feedback");
const nextButton = document.getElementById("next-btn");
const scoreElement = document.getElementById("score");
const progressElement = document.getElementById("progress");

// 初始化测验  // 页面加载后会调用
function initQuiz() {
  // 初始化入口函数开始
  loadQuestion(); // 加载当前题（默认第0题）
  updateProgress(); // 更新‘问题 x / y”的进度显示
}

// 加载问题
function loadQuestion() {
  // 把题目和选项渲染到页面
  const question = questions[currentQuestion]; // 取出当前题对象
  questionElement.textContent = question.question; // 把题目文本写入页面
  optionsElement.innerHTML = ""; // 清空上一题的选项按钮

  // 创建选项按钮
  question.options.forEach((option) => {
    // 遍历 traversal 当前题的每个选项
    const button = document.createElement("button");
    button.textContent = option; // 按钮显示选项文字
    button.addEventListener("click", () => selectAnswer(option));
    optionsElement.appendChild(button); // 把按钮加入到选项容器中
  });

  // 重置反馈和按钮状态
  feedbackElement.textContent = ""; // 清空上一题的反馈文字
  nextButton.style.display = "none"; // 默认隐藏“下一题”按钮（选完才显示）
  selectedOption = null; // 重置：当前题尚未选择答案
}

// 选择答案  // 用户点击选项按钮会触发
function selectAnswer(choice) {
  // 选择答案函数开始
  if (selectedOption !== null) return; // 防止重复选择

  selectedOption = choice; // 记录用户选择的选项
  const question = questions[currentQuestion]; // 取出当前题对象（用于读取正确答案）
  const buttons = optionsElement.querySelectorAll("button"); // 获取本题所有选项按钮节点列表

  // 禁用所有按钮
  buttons.forEach((btn) => {
    btn.disabled = true; // 禁用按钮：避免再次点击改变结果
    btn.classList.add("disabled"); // 加 disabled 类：用于CSS显示灰掉/不可点样式
  });

  // 显示正确/错误样式
  buttons.forEach((btn) => {
    // 再遍历一遍按钮，用于标记对错样式
    if (btn.textContent === question.answer) {
      // 如果这个按钮文字等于正确答案
      btn.classList.add("correct"); // 添加 正确 类：显示“正确答案”样式
    } else if (btn.textContent === choice && choice !== question.answer) {
      //选错了
      btn.classList.add("wrong"); // 加 错误 类：显示“错误答案”样式
    }
  });

  // 更新分数和显示反馈
  if (choice === question.answer) {
    // 判断：用户是否答对
    score++; // 答对：分数+1
    feedbackElement.textContent = "✅ 正确！";
    feedbackElement.style.color = "#4CAF50";
  } else {
    //答错
    feedbackElement.textContent = `❌ 错误！正确答案是: ${question.answer}`;
    feedbackElement.style.color = "#f44336";
  }

  // 显示下一题按钮
  nextButton.style.display = "inline-block"; // 选完后显示“下一题”按钮
}

// 下一题
function nextQuestion() {
  // 下一题函数开始
  currentQuestion++; // 当前题索引+1

  if (currentQuestion < questions.length) {
    // 如果还没到最后一题
    loadQuestion(); // 渲染下一题
    updateProgress(); // 更新进度显示
  } else {
    //要不就是做完题目了
    showResults();
  }
}

// 更新进度
function updateProgress() {
  // 更新进度函数开始
  progressElement.textContent = `问题 ${currentQuestion + 1} / ${questions.length}`; // 显示当前题号（索引+1）和总题数
}

// 显示结果// 题目全部完成后调用
function showResults() {
  questionElement.textContent = "测验完成！";
  optionsElement.innerHTML = ""; // 清空选项区域
  feedbackElement.textContent = ""; // 清空反馈区域
  nextButton.style.display = "none"; // 隐藏“下一题”按钮

  scoreElement.textContent = `🎯 最终得分: ${score} / ${questions.length}`;
  scoreElement.style.display = "block";
  显示分数区域;

  // 根据分数显示不同消息
  let message = "";
  if (score === questions.length) {
    message = "太棒了！你是中文大师！🌟";
  } else if (score >= questions.length * 0.7) {
    message = "做得很好！继续加油！👍";
  } else {
    message = "再接再厉！继续学习会更好的！💪";
  }

  const messageElement = document.createElement("div"); // 创建一个div用于显示评语
  messageElement.textContent = message; // 写入评语文本
  messageElement.style.marginTop = "20px";
  messageElement.style.fontSize = "20px";
  messageElement.style.fontWeight = "bold"; // 加粗
  scoreElement.parentNode.insertBefore(
    messageElement,
    scoreElement.nextSibling,
  ); // 把评语插入到分数后面
}

// 重置测验
function resetQuiz() {
  // 重置函数开始
  currentQuestion = 0; //第0题
  score = 0;
  selectedOption = null; // 清空选择状态
  scoreElement.style.display = "none"; //分数部分先不显示
  initQuiz(); //重新初始化（加载第一题 + 更新进度）
}

// 添加重置按钮  重新测试
const resetButton = document.createElement("button");
resetButton.textContent = "重新开始测验";
resetButton.className = "next-btn reset-btn";
resetButton.addEventListener("click", resetQuiz);
document.querySelector(".quiz").appendChild(resetButton);

// 页面加载完成后初始化测验
document.addEventListener("DOMContentLoaded", initQuiz);
