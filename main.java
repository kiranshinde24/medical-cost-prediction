import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.Random;

public class TypingTestFrame extends JFrame {

    private CardLayout cardLayout;
    private JPanel cardPanel;
    private JPanel page1;
    private JPanel page2;

    private JTextPane displayTextPane;
    private JTextField typingField;
    private JLabel resultLabel;
    private String textToType;
    private int timeElapsed;
    private Timer timer;

    public TypingTestFrame() {
        initializeUI();
    }

    private void initializeUI() {
        // Frame setup
        setTitle("Typing Speed Test");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(600, 450);
        setLocationRelativeTo(null);

        // CardLayout for switching pages
        cardLayout = new CardLayout();
        cardPanel = new JPanel(cardLayout);

        // Page 1 setup (selection of sentence or paragraph)
        page1 = new JPanel();
        page1.setLayout(new BorderLayout());
        
        JLabel headingLabel = new JLabel("Typing Speed Test", JLabel.CENTER);
        headingLabel.setFont(new Font("Arial", Font.BOLD, 18));
        page1.add(headingLabel, BorderLayout.NORTH);
        
        JPanel optionsPanel = new JPanel();
        optionsPanel.setLayout(new GridLayout(3, 1));
        
        JRadioButton sentenceRadioButton = new JRadioButton("Sentence");
        JRadioButton paragraphRadioButton = new JRadioButton("Paragraph");
        ButtonGroup group = new ButtonGroup();
        group.add(sentenceRadioButton);
        group.add(paragraphRadioButton);

        optionsPanel.add(sentenceRadioButton);
        optionsPanel.add(paragraphRadioButton);

        page1.add(optionsPanel, BorderLayout.CENTER);

        JButton startButton = new JButton("Start");
        startButton.addActionListener(e -> {
            if (sentenceRadioButton.isSelected()) {
                loadText("sentence");
            } else if (paragraphRadioButton.isSelected()) {
                loadText("paragraph");
            }
            cardLayout.show(cardPanel, "page2");
        });

        page1.add(startButton, BorderLayout.SOUTH);
        
        // Page 2 setup (typing test UI)
        page2 = new JPanel();
        page2.setLayout(new BorderLayout());
        
        displayTextPane = new JTextPane();
        displayTextPane.setEditable(false);
        displayTextPane.setFont(new Font("Serif", Font.PLAIN, 16));
        page2.add(new JScrollPane(displayTextPane), BorderLayout.NORTH);

        typingField = new JTextField();
        typingField.setEnabled(false);
        page2.add(typingField, BorderLayout.CENTER);

        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout());

        JButton startTestButton = new JButton("Start Test");
        startTestButton.addActionListener(e -> startTypingTest());
        buttonPanel.add(startTestButton);

        JButton resetButton = new JButton("Reset");
        resetButton.addActionListener(e -> resetTypingTest());
        buttonPanel.add(resetButton);

        JButton exitButton = new JButton("Exit");
        exitButton.addActionListener(e -> System.exit(0));
        buttonPanel.add(exitButton);

        page2.add(buttonPanel, BorderLayout.SOUTH);

        resultLabel = new JLabel("Results will be shown here.");
        resultLabel.setHorizontalAlignment(SwingConstants.CENTER);
        page2.add(resultLabel, BorderLayout.PAGE_END);

        // Adding both pages to the cardPanel
        cardPanel.add(page1, "page1");
        cardPanel.add(page2, "page2");

        // Adding cardPanel to JFrame
        add(cardPanel);

        // Show the first page initially
        cardLayout.show(cardPanel, "page1");
    }

    private void loadText(String mode) {
        Random random = new Random();
        if ("sentence".equals(mode)) {
            String[] sentences = {
                "The quick brown fox jumps over the lazy dog.",
                "Java programming is fun.",
                "Practice makes perfect."
            };
            textToType = sentences[random.nextInt(sentences.length)];
        } else if ("paragraph".equals(mode)) {
            String[] paragraphs = {
                "Java is a high-level programming language developed by Sun Microsystems. It is class-based, object-oriented, and designed to have as few implementation dependencies as possible.",
                "Typing tests are great tools for improving speed and accuracy. They also help reduce errors over time and boost typing confidence."
            };
            textToType = paragraphs[random.nextInt(paragraphs.length)];
        }

        displayTextPane.setText(textToType);
    }

    private void startTypingTest() {
        timeElapsed = 0;
        typingField.setEnabled(true);
        typingField.setText("");
        resultLabel.setText("Typing in progress...");
        typingField.requestFocus();

        timer = new Timer();
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                timeElapsed++;
            }
        }, 0, 1000);
    }

    private void resetTypingTest() {
        if (timer != null) {
            timer.cancel();
        }

        timeElapsed = 0;
        typingField.setText("");
        typingField.setEnabled(false);
        resultLabel.setText("Results will be shown here.");
        loadText("sentence");  // Default to sentence mode
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new TypingTestFrame().setVisible(true));
    }
}
