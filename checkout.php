<?php
include 'components/connect.php';
session_start();

if(isset($_SESSION['user_id'])){
   $user_id = $_SESSION['user_id'];
}else{
   $user_id = '';
   header('location:user_login.php');
}

// Function for AI verification
function verifyOrder($data) {
    $azureFeatures = [
        $data['typing_speed'],
        $data['time_on_page'],
        get_user_order_count($data['user_id'])
    ];

    // Call Flask API
    $ch = curl_init('http://localhost:5000/verify');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    $response = curl_exec($ch);
    curl_close($ch);

    $localResult = json_decode($response, true);

    // Dummy Azure result for now
    $azureResult = ['is_anomaly' => false];

    if ($localResult['decision'] === 'block' || $azureResult['is_anomaly']) {
        // log_fraud_attempt($data, $localResult, $azureResult); // Implement as needed
        return $localResult;
    }
    return $localResult;
}

function get_user_order_count($user_id) {
    // TODO: Implement actual logic to fetch order count from DB
    return 1;
}

if(isset($_POST['order'])){
   // Get AI verification metrics
   $typing_speed = $_POST['typing_speed'];
   $time_on_page = $_POST['time_on_page'];
   $method = $_POST['method'];

   // Verify order through AI
   $verification = verifyOrder([
       'typing_speed' => $typing_speed,
       'time_on_page' => $time_on_page,
       'payment_type' => $method,
       'user_id' => $user_id
   ]);

   if($verification['decision'] === 'allow') {
      // Your existing order processing code
      $name = filter_var($_POST['name'], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
      $number = filter_var($_POST['number'], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
      $email = filter_var($_POST['email'], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
      $address = 'flat no. '. $_POST['flat'] .', '. $_POST['street'] .', '. $_POST['city'] .', '. $_POST['Province'] .', '. $_POST['country'] .' - '. $_POST['pin_code'];
      $address = filter_var($address, FILTER_SANITIZE_FULL_SPECIAL_CHARS);
      $total_products = $_POST['total_products'];
      $total_price = $_POST['total_price'];

      $check_cart = $conn->prepare("SELECT * FROM `cart` WHERE user_id = ?");
      $check_cart->execute([$user_id]);

      if($check_cart->rowCount() > 0){
         $insert_order = $conn->prepare("INSERT INTO `orders`(user_id, name, number, email, method, address, total_products, total_price) VALUES(?,?,?,?,?,?,?,?)");
         $insert_order->execute([$user_id, $name, $number, $email, $method, $address, $total_products, $total_price]);

         $delete_cart = $conn->prepare("DELETE FROM `cart` WHERE user_id = ?");
         $delete_cart->execute([$user_id]);

         $message[] = 'order placed successfully!';
      }else{
         $message[] = 'your cart is empty';
      }
   } else {
      $message[] = 'Order verification failed: ' . $verification['reason'];
   }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>checkout</title>
   
   <!-- font awesome cdn link  -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">

   <!-- custom css file link  -->
   <link rel="stylesheet" href="css/style.css">

</head>
<body>
   
<?php include 'components/user_header.php'; ?>

<section class="checkout-orders">

   <form action="" method="POST">

   <h3>Your Orders</h3>

      <div class="display-orders">
      <?php
         $grand_total = 0;
         $cart_items[] = '';
         $select_cart = $conn->prepare("SELECT * FROM `cart` WHERE user_id = ?");
         $select_cart->execute([$user_id]);
         if($select_cart->rowCount() > 0){
            while($fetch_cart = $select_cart->fetch(PDO::FETCH_ASSOC)){
               $cart_items[] = $fetch_cart['name'].' ('.$fetch_cart['price'].' x '. $fetch_cart['quantity'].') - ';
               $total_products = implode($cart_items);
               $grand_total += ($fetch_cart['price'] * $fetch_cart['quantity']);
      ?>
         <p> <?= $fetch_cart['name']; ?> <span>(<?= '$'.$fetch_cart['price'].'/- x '. $fetch_cart['quantity']; ?>)</span> </p>
      <?php
            }
         }else{
            echo '<p class="empty">your cart is empty!</p>';
         }
      ?>
         <input type="hidden" name="total_products" value="<?= $total_products; ?>">
         <input type="hidden" name="total_price" value="<?= $grand_total; ?>" value="">
         <div class="grand-total">Grand Total : <span>rs.<?= $grand_total; ?>/-</span></div>
      </div>

      <h3>place your orders</h3>

      <div class="flex">
         <div class="inputBox">
            <span>Enter Your Name Here :</span>
            <input type="text" name="name" placeholder="enter your name" class="box" maxlength="20" required>
         </div>
         <div class="inputBox">
            <span>Your Number :</span>
            <input type="number" name="number" placeholder="enter your number" class="box" min="0" max="9999999999" onkeypress="if(this.value.length == 10) return false;" required>
         </div>
         <div class="inputBox">
            <span>Your Email :</span>
            <input type="email" name="email" placeholder="enter your email" class="box" maxlength="50" required>
         </div>
         <div class="inputBox">
            <span>Payment Option? :</span>
            <select name="method" class="box" required>
               <option value="cash on delivery">Cash On Delivery</option>
               <option value="credit card">Credit Card</option>
               <option value="paytm">paytm</option>
               <option value="paypal">Paypal</option>
            </select>
         </div>
         <div class="inputBox">
            <span>Address line 01 :</span>
            <input type="text" name="flat" placeholder="e.g. Home" class="box" maxlength="50" required>
         </div>
         <div class="inputBox">
            <span>Address line 02 :</span>
            <input type="text" name="street" placeholder="Street name" class="box" maxlength="50" required>
         </div>
         <div class="inputBox">
            <span>City :</span>
            <input type="text" name="city" placeholder="Kalmunai" class="box" maxlength="50" required>
         </div>
         <div class="inputBox">
            <span>Province:</span>
            <input type="text" name="Province" placeholder="Eastern" class="box" maxlength="50" required>
         </div>
         <div class="inputBox">
            <span>Country :</span>
            <input type="text" name="country" placeholder="Sri Lanka" class="box" maxlength="50" required>
         </div>
         <div class="inputBox">
            <span>ZIP CODE :</span>
            <input type="number" min="0" name="pin_code" placeholder="e.g. 56400" min="0" max="999999" onkeypress="if(this.value.length == 6) return false;" class="box" required>
         </div>
      </div>

      <input type="submit" name="order" class="btn <?= ($grand_total > 1)?'':'disabled'; ?>" value="place order">

   </form>

   <!-- Accuracy Control Section -->
   <div class="accuracy-control" style="margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
      <h3>AI Verification Accuracy Control</h3>
      <div class="accuracy-info">
         <p><strong>Current Target Accuracy:</strong> <span id="current-accuracy">85.0%</span></p>
         <p><strong>Original Accuracy:</strong> 98.7%</p>
         <p><strong>Accuracy Reduction:</strong> <span id="accuracy-reduction">13.7%</span></p>
      </div>
      
      <div class="accuracy-controls">
         <label>
            <input type="checkbox" id="accuracy-enabled" checked> Enable Accuracy Reduction
         </label>
         <br><br>
         <label>Target Accuracy: <input type="range" id="target-accuracy" min="70" max="95" value="85" step="5"> <span id="target-display">85%</span></label>
         <br><br>
         <label>Noise Factor: <input type="range" id="noise-factor" min="0" max="30" value="15" step="5"> <span id="noise-display">15%</span></label>
         <br><br>
         <label>Bias Factor: <input type="range" id="bias-factor" min="0" max="20" value="10" step="5"> <span id="bias-display">10%</span></label>
         <br><br>
         <button type="button" id="update-accuracy" class="btn">Update Accuracy Settings</button>
      </div>
   </div>

</section>

<?php include 'components/footer.php'; ?>

<script src="js/script.js"></script>
<script>
let startTime = Date.now();
let keystrokes = 0;

document.querySelectorAll('input[type="text"], input[type="email"], input[type="number"]').forEach(input => {
    input.addEventListener('keypress', () => {
        keystrokes++;
    });
});

document.querySelector('form').addEventListener('submit', (e) => {
    let timeOnPage = Math.round((Date.now() - startTime) / 1000);
    let typingSpeed = Math.round((keystrokes / timeOnPage) * 60);

    let typingSpeedInput = document.createElement('input');
    typingSpeedInput.type = 'hidden';
    typingSpeedInput.name = 'typing_speed';
    typingSpeedInput.value = typingSpeed;
    document.querySelector('form').appendChild(typingSpeedInput);

    let timeOnPageInput = document.createElement('input');
    timeOnPageInput.type = 'hidden';
    timeOnPageInput.name = 'time_on_page';
    timeOnPageInput.value = timeOnPage;
    document.querySelector('form').appendChild(timeOnPageInput);
});

// Accuracy Control JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Update displays when sliders change
    document.getElementById('target-accuracy').addEventListener('input', function() {
        document.getElementById('target-display').textContent = this.value + '%';
        updateAccuracyReduction();
    });
    
    document.getElementById('noise-factor').addEventListener('input', function() {
        document.getElementById('noise-display').textContent = this.value + '%';
    });
    
    document.getElementById('bias-factor').addEventListener('input', function() {
        document.getElementById('bias-display').textContent = this.value + '%';
    });
    
    // Update accuracy reduction display
    function updateAccuracyReduction() {
        const targetAccuracy = parseFloat(document.getElementById('target-accuracy').value);
        const originalAccuracy = 98.7;
        const reduction = originalAccuracy - targetAccuracy;
        document.getElementById('accuracy-reduction').textContent = reduction.toFixed(1) + '%';
        document.getElementById('current-accuracy').textContent = targetAccuracy.toFixed(1) + '%';
    }
    
    // Update accuracy settings
    document.getElementById('update-accuracy').addEventListener('click', function() {
        const enabled = document.getElementById('accuracy-enabled').checked;
        const targetAccuracy = parseFloat(document.getElementById('target-accuracy').value) / 100;
        const noiseFactor = parseFloat(document.getElementById('noise-factor').value) / 100;
        const biasFactor = parseFloat(document.getElementById('bias-factor').value) / 100;
        
        fetch('http://localhost:5000/accuracy-control', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                enabled: enabled,
                target_accuracy: targetAccuracy,
                noise_factor: noiseFactor,
                bias_factor: biasFactor
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Accuracy settings updated successfully!');
                console.log('Accuracy settings:', data.accuracy_reduction);
            } else {
                alert('Failed to update accuracy settings');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating accuracy settings. Make sure the Flask API is running.');
        });
    });
    
    // Load current settings on page load
    fetch('http://localhost:5000/accuracy-control')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const settings = data.accuracy_reduction;
                document.getElementById('accuracy-enabled').checked = settings.enabled;
                document.getElementById('target-accuracy').value = Math.round(settings.target_accuracy * 100);
                document.getElementById('noise-factor').value = Math.round(settings.random_noise_factor * 100);
                document.getElementById('bias-factor').value = Math.round(settings.bias_factor * 100);
                
                // Update displays
                document.getElementById('target-display').textContent = Math.round(settings.target_accuracy * 100) + '%';
                document.getElementById('noise-display').textContent = Math.round(settings.random_noise_factor * 100) + '%';
                document.getElementById('bias-display').textContent = Math.round(settings.bias_factor * 100) + '%';
                updateAccuracyReduction();
            }
        })
        .catch(error => {
            console.log('Could not load accuracy settings. API may not be running.');
        });
});
</script>

</body>
</html>